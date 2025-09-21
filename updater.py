#!/usr/bin/env python3
import os
import re
import subprocess
import urllib.parse
from datetime import datetime

# Configuration
WRITEUPS_DIR = "Resources/Personal/Write-ups"
README_PATH = "README.md"
LATEST_SECTION_HEADER = "## 🔍 Latest Blog Posts"
GITHUB_BASE_URL = "https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main"

# GitHub-flavored Markdown table header (required header + separator)
TABLE_HEADER = (
    "| Platform | Lab | Category | Date Posted |\n"
    "| --- | --- | --- | --- |\n"
)

# Regex helpers
ROW_RE = re.compile(
    r"^\|\s*(?P<platform>.+?)\s*\|\s*(?P<lab>.+?)\s*\|\s*(?P<category>.+?)\s*\|\s*(?P<date>\d{2}-\d{2}-\d{4})\s*\|$"
)

def url_for_rel(rel_path: str) -> str:
    # Encode path segments but keep "/" intact for GitHub URLs
    encoded = urllib.parse.quote(rel_path, safe="/")
    return f"{GITHUB_BASE_URL}/{encoded}"

def get_writeup_readmes(directory: str):
    """Find all readme.md under WRITEUPS_DIR (case-insensitive)."""
    found = []
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return found
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower() == "readme.md":
                found.append(os.path.join(root, f))
    return found

def parse_platform_category_lab(rel_path: str):
    """
    Map repo paths to (platform, category, lab).
    Handles:
      - Resources/.../Write-ups/Platform/Category/Lab/README.md
      - Resources/.../Write-ups/Platform/<group>/Category/Lab/README.md
    Uses the directory before Lab as Category so deeper trees still resolve correctly.
    """
    parts = rel_path.split("/")
    try:
        base_idx = parts.index("Write-ups")
    except ValueError:
        return None
    rest = parts[base_idx + 1 :]  # after "Write-ups"
    # Need at least Platform, ..., Category, Lab, README.md
    if len(rest) < 4 or rest[-1].lower() != "readme.md":
        return None
    platform = rest[0]
    lab = rest[-2]                 # folder that contains README.md
    category = rest[-3]            # folder before Lab, supports deeper trees
    return platform, category, lab

def generate_table_rows(paths, today_str):
    """
    For each README path, build a Markdown table row:
      | [Platform](url) | [Lab](url) | Category | MM-DD-YYYY |
    Both Platform and Lab cells link to the GitHub web view of that README path.
    """
    rows = []
    for p in sorted(paths):
        rel_path = os.path.relpath(p, ".").replace("\\", "/")
        pcl = parse_platform_category_lab(rel_path)
        if not pcl:
            continue
        platform, category, lab = pcl
        url = url_for_rel(rel_path)
        plat_md = f"[{platform}]({url})"
        lab_md = f"[{lab}]({url})"
        row = f"| {plat_md} | {lab_md} | {category} | {today_str} |"
        rows.append((row, url))
    return rows

def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def parse_section(readme_content: str):
    """
    Split README into: prefix (up to and including header line),
                       section_body (content after header until next H1/H2 or EOF),
                       suffix (rest).
    If the header is missing, create it at the top.
    """
    idx = readme_content.find(LATEST_SECTION_HEADER)
    if idx == -1:
        # No header found; put it at the top
        return LATEST_SECTION_HEADER + "\n\n", "", readme_content
    after = readme_content[idx + len(LATEST_SECTION_HEADER):]
    # Find next H1/H2 after header to bound the section
    m = re.search(r"(?m)^(#{1,2})\s+", after)
    if m:
        split_pos = idx + len(LATEST_SECTION_HEADER) + m.start()
        prefix = readme_content[:idx] + LATEST_SECTION_HEADER + "\n\n"
        section_body = readme_content[idx + len(LATEST_SECTION_HEADER):split_pos]
        suffix = readme_content[split_pos:]
    else:
        prefix = readme_content[:idx] + LATEST_SECTION_HEADER + "\n\n"
        section_body = readme_content[idx + len(LATEST_SECTION_HEADER):]
        suffix = ""
    return prefix, section_body.strip("\n"), suffix

def extract_existing_urls_from_table(section_body: str):
    """
    Collect all URLs from Markdown links within the table block (any line with | ... and ](URL)).
    This is used for deduplication across reruns.
    """
    urls = set()
    for line in section_body.splitlines():
        if "](" in line and line.strip().startswith("|"):
            for match in re.finditer(r"\]\((https?://[^\)]+)\)", line):
                urls.add(match.group(1))
    return urls

def build_table(existing_body: str, candidate_rows):
    """
    Build a table that prepends new rows (by unique URL) above existing rows,
    preserving previous entries and their original dates.
    """
    existing_urls = extract_existing_urls_from_table(existing_body)
    new_rows = [r for r, u in candidate_rows if u not in existing_urls]

    # Extract any existing table rows after header/separator if present
    existing_lines = [ln for ln in existing_body.splitlines() if ln.strip()]
    existing_table_rows = []
    if existing_lines and existing_lines[0].strip().startswith("|"):
        # Detect a header + separator structure and skip them
        start_idx = 0
        if len(existing_lines) >= 2 and existing_lines[1].strip().startswith("|"):
            start_idx = 2
        existing_table_rows = existing_lines[start_idx:]

    # Compose the table
    table = TABLE_HEADER
    if new_rows:
        table += "\n".join(new_rows)
        if existing_table_rows:
            table += "\n"
    if existing_table_rows:
        table += "\n".join(existing_table_rows)
    # Ensure trailing newline
    if not table.endswith("\n"):
        table += "\n"
    return table

def configure_git():
    """Set git identity if missing to allow committing in CI/local."""
    try:
        result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
        if not result.stdout.strip():
            subprocess.run(["git", "config", "user.name", "L0WK3Y-IAAN"], check=True)
            print("Configured git user.name.")
        result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
        if not result.stdout.strip():
            subprocess.run(["git", "config", "user.email", "you@example.com"], check=True)
            print("Configured git user.email.")
    except subprocess.CalledProcessError as e:
        print("Failed to configure Git user information:")
        print(e.stderr)
        exit(1)

def main():
    configure_git()

    paths = get_writeup_readmes(WRITEUPS_DIR)
    if not paths:
        print(f"No 'readme.md' files found under '{WRITEUPS_DIR}'. Exiting.")
        return

    today_str = datetime.now().strftime("%m-%d-%Y")
    candidate_rows = generate_table_rows(paths, today_str)

    if not os.path.exists(README_PATH):
        print(f"Could not find '{README_PATH}' in the current directory. Exiting.")
        return

    original = read_file(README_PATH)
    prefix, section_body, suffix = parse_section(original)

    merged_table = build_table(section_body, candidate_rows)
    updated = prefix + merged_table + "\n" + suffix

    if updated != original:
        write_file(README_PATH, updated)
        print("README updated with new entries. Committing changes...")
        subprocess.run(["git", "add", README_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "🟢 New Write-up Added!"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    else:
        print("No changes detected in README.md.")

if __name__ == "__main__":
    main()
