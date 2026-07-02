#!/usr/bin/env python3
"""Send a test chat completion request to the local LiteLLM proxy."""

import json
from pathlib import Path
from urllib.request import Request, urlopen


def read_api_key(env_path: Path) -> str:
    """Return LITELLM_CLAUDE_KEY if set, otherwise LITELLM_MASTER_KEY."""
    if not env_path.exists():
        return ""
    claude_key = master_key = ""
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("LITELLM_CLAUDE_KEY="):
            val = line.split("=", 1)[1].strip().strip('"')
            if val:
                claude_key = val
        elif line.startswith("LITELLM_MASTER_KEY="):
            master_key = line.split("=", 1)[1].strip().strip('"')
    return claude_key or master_key


def main() -> int:
    key = read_api_key(Path(".env"))
    if not key:
        raise SystemExit("No API key found in .env — run 'run setup' first")

    payload = json.dumps(
        {
            "model": "claude-haiku-4-5",
            "messages": [{"role": "user", "content": "Say 'Hello from LiteLLM proxy!' and nothing else."}],
        }
    ).encode("utf-8")

    req = Request(
        "http://localhost:4444/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )

    with urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
