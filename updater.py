#!/usr/bin/env python3
import os
import re
import subprocess
import urllib.parse
import json
from datetime import datetime

# Configuration - now supporting multiple READMEs
WRITEUPS_DIR = "Resources/Personal/Write-ups"
README_PATHS = [
    "README.md",  # Root README
    "Resources/README.md",  # Resources README  
    "Resources/Personal/Write-ups/README.md"  # Write-ups README
]
JSON_OUTPUT_PATH = "writeups.json"  # JSON file for the interactive table
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
    """Find all markdown files under WRITEUPS_DIR that represent writeups."""
    found = []
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return found
    for root, dirs, files in os.walk(directory):
        for f in files:
            # Accept readme.md (any case) or any .md file in a numbered/named folder
            if f.lower() == "readme.md" or f.lower().endswith(".md"):
                # Skip the main Write-ups/README.md itself
                if root.endswith("Write-ups") and f.lower() == "readme.md":
                    continue
                found.append(os.path.join(root, f))
    return found

def parse_platform_category_lab(rel_path: str):
    """
    Map repo paths to (platform, category, lab).
    Handles:
      - Resources/.../Write-ups/Platform/Category/Lab/README.md
      - Resources/.../Write-ups/Platform/Category/Lab/anything.md
      - Resources/.../Write-ups/Platform/<group>/Category/Lab/README.md
    Uses the directory before the .md file as Lab, supporting deeper trees.
    """
    parts = rel_path.split("/")
    try:
        base_idx = parts.index("Write-ups")
    except ValueError:
        return None
    rest = parts[base_idx + 1 :]  # after "Write-ups"
    # Need at least Platform, ..., Category, Lab, file.md
    if len(rest) < 4 or not rest[-1].lower().endswith(".md"):
        return None
    platform = rest[0]
    lab = rest[-2]                 # folder that contains the .md file
    category = rest[-3]            # folder before Lab, supports deeper trees
    return platform, category, lab

def generate_table_rows(paths, today_str):
    """
    For each README path, build a Markdown table row:
      | [Platform] | [Lab](url) | Category | MM-DD-YYYY |
    Both Platform and Lab cells link to the GitHub web view of that README path.
    Returns list of (row_string, url, lab_name) tuples.
    """
    rows = []
    for p in sorted(paths):
        rel_path = os.path.relpath(p, ".").replace("\\", "/")
        pcl = parse_platform_category_lab(rel_path)
        if not pcl:
            continue
        platform, category, lab = pcl
        url = url_for_rel(rel_path)
        plat_md = f"{platform}"
        lab_md = f"[{lab}]({url})"
        row = f"| {plat_md} | {lab_md} | {category} | {today_str} |"
        rows.append((row, url, lab))
    return rows

def generate_json_data(paths):
    """
    Generate JSON data from all writeups with their existing dates from README.
    Returns list of writeup dictionaries with platform, lab, category, date, and url.
    """
    writeups_data = []
    
    # First, try to load existing dates from the main README
    existing_dates = {}
    if os.path.exists("README.md"):
        readme_content = read_file("README.md")
        _, section_body, _ = parse_section(readme_content)
        
        # Extract existing dates from the table
        for line in section_body.splitlines():
            line = line.strip()
            if not line or not line.startswith("|"):
                continue
            if "---" in line or "Platform" in line:
                continue
            
            # Parse the table row to get lab name and date
            match = re.search(r"\|\s*[^|]+\|\s*\[([^\]]+)\][^|]*\|\s*[^|]+\|\s*(\d{2}-\d{2}-\d{4})\s*\|", line)
            if match:
                lab_name = match.group(1).strip().lower()
                date = match.group(2).strip()
                existing_dates[lab_name] = date
    
    # Generate data for all writeups
    for p in sorted(paths):
        rel_path = os.path.relpath(p, ".").replace("\\", "/")
        pcl = parse_platform_category_lab(rel_path)
        if not pcl:
            continue
        
        platform, category, lab = pcl
        url = url_for_rel(rel_path)
        
        # Use existing date if available, otherwise use today
        date = existing_dates.get(lab.lower(), datetime.now().strftime("%m-%d-%Y"))
        
        writeup_entry = {
            "platform": platform,
            "lab": lab,
            "category": category,
            "date": date,
            "url": url
        }
        writeups_data.append(writeup_entry)
    
    return writeups_data

def write_json_file(data, filepath):
    """Write JSON data to file with pretty formatting."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON data written to {filepath}")

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

def extract_existing_labs_from_table(section_body: str):
    """
    Extract lab names from existing table rows to avoid duplicates.
    Returns a set of lab names (case-insensitive).
    """
    labs = set()
    for line in section_body.splitlines():
        line = line.strip()
        if not line or not line.startswith("|"):
            continue
        # Skip header and separator rows
        if "---" in line or "Platform" in line:
            continue
        # Extract lab name from markdown link [Lab Name](url)
        match = re.search(r"\|\s*\[([^\]]+)\]", line)
        if match:
            labs.add(match.group(1).strip().lower())
    return labs

def build_table(existing_body: str, candidate_rows):
    """
    Build a table that prepends new rows (by unique lab name) above existing rows,
    preserving previous entries and their original dates.
    """
    existing_labs = extract_existing_labs_from_table(existing_body)
    
    # Filter new rows - only include if lab name is not already in table
    new_rows = []
    for row, url, lab in candidate_rows:
        if lab.lower() not in existing_labs:
            new_rows.append(row)
            print(f"  → Adding new entry: {lab}")

    # Extract any existing table rows after header/separator if present
    existing_lines = [ln for ln in existing_body.splitlines() if ln.strip()]
    existing_table_rows = []
    if existing_lines:
        # Skip header and separator rows
        for i, line in enumerate(existing_lines):
            if line.strip().startswith("|"):
                if "---" not in line and "Platform" not in line:
                    existing_table_rows.append(line)

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
    return table, len(new_rows) > 0

def process_readme(readme_path, candidate_rows):
    """Update a single README file with the table."""
    if not os.path.exists(readme_path):
        print(f"Could not find '{readme_path}'. Skipping.")
        return False
    
    print(f"Processing {readme_path}...")
    original = read_file(readme_path)
    prefix, section_body, suffix = parse_section(original)
    merged_table, has_new = build_table(section_body, candidate_rows)
    updated = prefix + merged_table + "\n" + suffix
    
    # Use has_new flag instead of string comparison
    if has_new:
        write_file(readme_path, updated)
        print(f"✅ Updated {readme_path}")
        return True
    else:
        print(f"ℹ️  No new entries for {readme_path}")
        return False


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

def has_git_changes():
    """Check if there are any staged changes to commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True
    )
    # Returns 0 if no changes, 1 if changes exist
    return result.returncode == 1


def main():
    configure_git()

    paths = get_writeup_readmes(WRITEUPS_DIR)
    if not paths:
        print(f"No 'readme.md' files found under '{WRITEUPS_DIR}'. Exiting.")
        return

    print(f"\n📝 Found {len(paths)} writeup(s) in {WRITEUPS_DIR}")
    
    # Debug: Show all found writeups
    print("\n🔍 Debug - Writeups found:")
    for p in sorted(paths):
        rel_path = os.path.relpath(p, ".").replace("\\", "/")
        pcl = parse_platform_category_lab(rel_path)
        if pcl:
            platform, category, lab = pcl
            print(f"  • {platform}/{category}/{lab}")
        else:
            print(f"  ⚠️  Could not parse: {rel_path}")
    
    today_str = datetime.now().strftime("%m-%d-%Y")
    candidate_rows = generate_table_rows(paths, today_str)
    
    print(f"\n📊 Generated {len(candidate_rows)} candidate row(s)\n")

    # Generate and write JSON data
    print("📄 Generating JSON data for interactive table...")
    json_data = generate_json_data(paths)
    write_json_file(json_data, JSON_OUTPUT_PATH)

    # Process each README file
    files_changed = []
    for readme_path in README_PATHS:
        if process_readme(readme_path, candidate_rows):
            files_changed.append(readme_path)

    # Add JSON file to changed files if it was created/updated
    if os.path.exists(JSON_OUTPUT_PATH):
        files_changed.append(JSON_OUTPUT_PATH)

    # Stage files and check if there are actual changes
    if files_changed:
        print(f"\n🚀 Files to check: {', '.join(files_changed)}")
        print("Staging files...")
        for file_path in files_changed:
            subprocess.run(["git", "add", file_path], check=True)
        
        # Check if there are actually staged changes
        if has_git_changes():
            print("Committing changes...")
            subprocess.run(["git", "commit", "-m", "🟢 New Write-up Added!"], check=True)
            subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
            print("✅ Changes pushed successfully!")
        else:
            print("ℹ️  No actual changes detected after staging (files unchanged).")
    else:
        print("\nℹ️  No changes detected in any README files.")


if __name__ == "__main__":
    main()