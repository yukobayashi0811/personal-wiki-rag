from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from .evidence import save_run
from .harness import PersonalWikiHarness
from .settings import Settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wiki",
        description="Offline personal wiki CLI powered by local Gemma and MLX-LM.",
    )
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Index sources and generate reviewed wiki-note drafts.")
    ingest.add_argument("source", nargs="?", type=Path, help="Optional source directory; defaults to vault/raw.")
    ingest.add_argument("--index-only", action="store_true", help="Skip Gemma wiki-note generation.")

    search = subparsers.add_parser("search", help="Return original passages without generating an answer.")
    search.add_argument("query")
    search.add_argument("--save", action="store_true", help="Save an evidence record.")

    ask = subparsers.add_parser("ask", help="Answer one standalone question from retrieved evidence.")
    ask.add_argument("question")
    ask.add_argument("--mode", choices=["local"], default="local")
    ask.add_argument("--no-save", action="store_true")

    chat = subparsers.add_parser("chat", help="Start the conversational personal assistant.")
    chat.add_argument("--save", action="store_true", help="Save each chat turn as evidence.")

    subparsers.add_parser("status", help="Show local configuration and index counts.")
    return parser


def _print_search_results(results) -> None:
    if not results:
        print("No matching passages found.")
        return
    for index, result in enumerate(results, start=1):
        print(f"[S{index}] vault/raw/{result.source_path} ({result.locator})")
        print(result.text)
        print()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    settings = Settings.from_environment(args.project_root)
    harness = PersonalWikiHarness(settings)

    try:
        if args.command == "ingest":
            if args.source and args.source.resolve() != settings.raw_dir.resolve():
                parser.error("This project preserves originals only from vault/raw; copy sources there first.")
            summary = harness.ingest(generate_notes=not args.index_only)
            print(json.dumps(summary, indent=2))
        elif args.command == "search":
            results = harness.search(args.query)
            _print_search_results(results)
            if args.save:
                output = "\n\n".join(result.text for result in results)
                save_run(settings.evidence_dir, "search", args.query, output, None, results)
        elif args.command == "ask":
            print(f"Model: {settings.model_id} | Execution: local")
            print(harness.ask(args.question, save=not args.no_save))
        elif args.command == "chat":
            print(f"Model: {settings.model_id} | Execution: local")
            print("Type /exit to quit or /help for chat guidance.")
            history: list[dict[str, str]] = []
            while True:
                try:
                    message = input("you> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if message == "/exit":
                    break
                if message == "/help":
                    print("Ask for drafting, planning, or ideas. Mention 'my notes' to retrieve wiki evidence.")
                    continue
                if not message:
                    continue
                answer = harness.chat_turn(message, history, save=args.save)
                print(f"wiki> {answer}")
                history.extend(
                    [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": answer},
                    ]
                )
        elif args.command == "status":
            from .store import WikiStore

            with WikiStore(settings.database_path) as store:
                print(f"Model: {settings.model_id}")
                print("Execution: local")
                print(f"Indexed documents: {store.document_count()}")
                print(f"Indexed passages: {store.chunk_count()}")
                print(f"Raw source directory: {settings.raw_dir}")
        return 0
    except (RuntimeError, ValueError, FileNotFoundError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

