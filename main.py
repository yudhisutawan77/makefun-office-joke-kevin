#!/usr/bin/env python3
"""The Funniest Office Joke, Judged Head to Head.

Writes one single-line office joke to the entry output and to stdout.

The joke: a setup ("my boss promised to ping me about the promotion")
with a turn on the double meaning of "ping" -- two years on, the only
ping that ever arrives is the microwave's. Punchline last, one line,
under the 200-character gate.
"""

import os
import sys

JOKE = (
    "My boss promised to ping me about the promotion; two years on, "
    "the only ping I get is the microwave in the break room."
)

DEFAULT_OUTPUT = "/output/entry.txt"


def resolve_output_path() -> str:
    """Return the file path the entry text goes to.

    $ENTRY_OUT may name a file or a directory: when it is a directory
    (existing, or a path with no file suffix) the entry lands in
    entry.txt inside it. Without $ENTRY_OUT, /output/entry.txt.
    """
    raw = os.environ.get("ENTRY_OUT") or DEFAULT_OUTPUT
    if os.path.isdir(raw):
        return os.path.join(raw, "entry.txt")
    return raw


def validate(text: str) -> str:
    """Enforce the gate: UTF-8 text of 1 to 200 characters, not blank."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("entry is blank")
    if len(stripped) > 200:
        raise ValueError(f"entry is {len(stripped)} chars, over the 200 cap")
    return stripped


def main() -> int:
    try:
        text = validate(JOKE)
    except ValueError as exc:
        print(f"entry invalid: {exc}", file=sys.stderr)
        return 1
    target = resolve_output_path()
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
