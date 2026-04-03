#!/usr/bin/env python3

import argparse
import json
import sys
from urllib import error, request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stream text from Ollama's /api/generate endpoint."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Why is the sky blue?",
        help="Prompt to send to the model.",
    )
    parser.add_argument(
        "--url",
        default="http://localhost:9090/api/generate",
        help="Ollama generate endpoint URL.",
    )
    parser.add_argument(
        "--model",
        default="gemma3:4b",
        help="Model name to request.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.dumps({"model": args.model, "prompt": args.prompt}).encode("utf-8")
    req = request.Request(
        args.url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue

                event = json.loads(line)

                if "error" in event:
                    print(event["error"], file=sys.stderr)
                    return 1

                chunk = event.get("response", "")
                if chunk:
                    print(chunk, end="", flush=True)

                if event.get("done"):
                    break
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except error.URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Failed to parse streamed JSON: {exc}", file=sys.stderr)
        return 1

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())