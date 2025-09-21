#!/usr/bin/env python3
import os
import re
import subprocess
import urllib.parse
from datetime import datetime

WRITEUPS_DIR = "Resources/Personal/Write-ups"
README_PATH = "README.md"
LATEST_SECTION_HEADER = "## 🔍 Latest Blog Posts"
GITHUB_BASE_URL = "https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main"

LINK_LINE_RE = re.compile(r"^- \[(?P<text>.+?)\]\((?P<url>https?://[^\)]+)\)\s+–\s+(?P<date>\d{2}-\d{2}-\d{4})\s*$")

def get_writeup_readmes(directory):
    found_readmes = []
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return found_readmes
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower() == "readme.md":
                found_readmes.append(os.path.join(root, f))
    return found_readmes

def build_link_line(path, today_str):
    folder_name = os.path.basename(os.path.dirname(path))
    rel_path = os.path.relpath(path, ".").replace("\\", "/")
    encoded_path = urllib.parse.quote(rel_path)
    final_url = f"{GITHUB_BASE_URL}/{encoded_path}"
    return f"- [{folder_name}]({final_url}) – {today_str}", final_url

def read_file(fp):
    with open(fp, "r", encoding="utf-8") as f:
        return f.read()

def write_file(fp, content):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

def parse_section(readme_content):
    """
    Returns: (prefix, section_body, suffix)
    Where section_body is the text after the header up to the next H2/H1 or EOF.
    """
    # Find header
    header_idx = readme_content.find(LATEST_SECTION_HEADER)
    if header_idx == -1:
        # If header missing, create it at top
        return "", "", readme_content
    # From header to end
    after = readme_content[header_idx:]
    # Find the next header start after current header line
    m = re.search(r"(?m)^(#{1,2})\s+", after[len(LATEST_SECTION_HEADER):])
    if m:
        split_pos = header_idx + len(LATEST_SECTION_HEADER) + m.start()
        prefix = readme_content[:header_idx]
        section_plus_header = readme_content[header_idx:split_pos]
        suffix = readme_content[split_pos:]
    else:
        prefix = readme_content[:header_idx]
        section_plus_header = readme_content[header_idx:]
        suffix = ""
    # Separate header line from body
    lines = section_plus_header.splitlines()
    # first line is header
    header_line = lines[0]
    body = "\n".join(lines[1:]).lstrip("\n")
    # Rebuild prefix to include header line
    new_prefix = prefix + header_line + "\n"
    return new_prefix, body, suffix

def extract_existing_urls(section_body):
    urls = set()
    for line in section_body.splitlines():
        m = LINK_LINE_RE.match(line.strip())
        if m:
            urls.add(m.group("url"))
    return urls

def merge_links(existing_body, new_lines):
    """
    Prepend only lines whose URL is not already present in existing_body.
    Preserve existing_body as-is to keep prior dates.
    """
    existing_urls = extract_existing_urls(existing_body)
    unique_new = []
    for line in new_lines:
        m = LINK_LINE_RE.match(line)
        url = None
        if m:
            url = m.group("url")
        else:
            # Fallback: try to pull URL via simple search
            url_match = re.search(r"\((https?://[^\)]+)\)", line)
            if url_match:
                url = url_match.group(1)
        if url and url not in existing_urls:
            unique_new.append(line)
    if not unique_new:
        return existing_body
    # Prepend new items above existing list, with a blank line after
    new_block = "\n".join(unique_new).rstrip()
    existing_body_clean = existing_body.lstrip("\n")
    if existing_body_clean:
        merged = new_block + "\n" + existing_body_clean
    else:
        merged = new_block + "\n"
    return merged

def configure_git():
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
    candidate_lines = []
    for p in sorted(paths):
        line, _url = build_link_line(p, today_str)
        candidate_lines.append(line)

    if not os.path.exists(README_PATH):
        print(f"Could not find '{README_PATH}' in the current directory. Exiting.")
        return

    original = read_file(README_PATH)
    prefix, section_body, suffix = parse_section(original)
    # Ensure there’s at least a blank line after header before entries
    if section_body and not section_body.startswith("\n"):
        section_body = "\n" + section_body

    merged_body = merge_links(section_body, candidate_lines)

    updated = prefix + merged_body.rstrip() + ("\n\n" if not merged_body.endswith("\n") else "\n") + suffix

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
