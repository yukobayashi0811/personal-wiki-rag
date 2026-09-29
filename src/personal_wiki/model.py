from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import psutil


@dataclass(frozen=True)
class GenerationMetrics:
    elapsed_seconds: float
    process_memory_before_gb: float
    process_memory_after_gb: float
    mlx_peak_memory_gb: float | None


@dataclass(frozen=True)
class GenerationResult:
    text: str
    metrics: GenerationMetrics


def clean_model_output(text: str) -> str:
    """Return only the user-visible final channel from Gemma output."""
    if "<channel|>" in text:
        text = text.rsplit("<channel|>", 1)[-1]
    for marker in ("<|channel>final", "<|channel>thought", "<turn|>", "<eos>"):
        text = text.replace(marker, "")
    return text.strip()


class LocalGemma:
    """Lazy MLX-LM adapter. The model is loaded only for generation commands."""

    def __init__(self, model_id: str):
        self.model_id = model_id
        self._model: Any = None
        self._tokenizer: Any = None

    def load(self) -> None:
        if self._model is not None:
            return
        try:
            from mlx_lm import load
        except ImportError as error:
            raise RuntimeError(
                "MLX-LM is missing or this platform is unsupported. "
                "Install the project on an Apple Silicon Mac."
            ) from error

        try:
            self._model, self._tokenizer = load(self.model_id)
        except Exception as error:
            raise RuntimeError(
                f"The model '{self.model_id}' is not available in the local cache. "
                f"While online, run: hf download {self.model_id}"
            ) from error

    def generate(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 700,
        temperature: float = 0.2,
    ) -> GenerationResult:
        self.load()
        try:
            from mlx_lm import generate
            from mlx_lm.sample_utils import make_sampler
        except ImportError as error:
            raise RuntimeError(
                "MLX-LM is missing or this platform is unsupported. "
                "Install the project on an Apple Silicon Mac."
            ) from error

        prompt = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        # Gemma 4 supports explicit thought and final channels. Starting the final
        # channel keeps private reasoning out of saved answers and avoids spending
        # the assignment's output budget on hidden deliberation.
        prompt += "<|channel>final\n"
        process = psutil.Process()
        before = process.memory_info().rss / 1_000_000_000
        started = time.perf_counter()
        text = clean_model_output(generate(
            self._model,
            self._tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            sampler=make_sampler(temp=temperature),
            verbose=False,
        ))
        elapsed = time.perf_counter() - started
        after = process.memory_info().rss / 1_000_000_000
        mlx_peak_memory_gb = None
        try:
            import mlx.core as mx

            getter = getattr(mx, "get_peak_memory", None)
            if getter is None and hasattr(mx, "metal"):
                getter = getattr(mx.metal, "get_peak_memory", None)
            if getter is not None:
                mlx_peak_memory_gb = float(getter()) / 1_000_000_000
        except (ImportError, AttributeError, RuntimeError, TypeError, ValueError):
            mlx_peak_memory_gb = None
        return GenerationResult(
            text=text,
            metrics=GenerationMetrics(elapsed, before, after, mlx_peak_memory_gb),
        )
