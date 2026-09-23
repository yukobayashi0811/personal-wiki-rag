# Local Model Smoke Test

- Runtime: `MLX-LM 0.31.3`
- Python: `3.13`
- Model: `mlx-community/gemma-4-e4b-it-4bit`
- Snapshot revision: `475b9088d29754a3379866cf5aeb6b41acd313c2`
- Execution: local Apple Silicon
- Device: MacBook Air, Apple M5, 32 GB unified memory

## Prompt

> In one sentence, explain what retrieval-augmented generation does.

## Actual Output

> Retrieval-augmented generation enhances large language models by retrieving relevant, up-to-date information from an external knowledge base and integrating it into the prompt to improve the accuracy and grounding of the generated output.

## Measurements

- Generation time: `1.18 seconds`
- Process resident memory before generation: `4.68 GB`
- Process resident memory after generation: `4.69 GB`
- System-wide free-memory percentage after model setup: `82%`
- Free disk space after model download: `19 GiB`

This smoke test proves that the model loads and generates locally. It is not a final assignment evaluation. Final memory and response-time measurements must use the selected wiki sources and include one ingestion run and one ask-mode answer.

