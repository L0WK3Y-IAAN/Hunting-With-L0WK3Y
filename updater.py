#!/usr/bin/env python3
import os
import re
import subprocess
import urllib.parse
from datetime import datetime  # <-- for appending today's date

# Adjust these constants to your project
WRITEUPS_DIR = "Resources/Personal/Write-ups"  
README_PATH = "README.md"
LATEST_SECTION_HEADER = "## 🔍 Latest Blog Posts"
GITHUB_BASE_URL = "https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main"

def get_writeup_readmes(directory):
    """
    Recursively scan `directory` for any 'readme.md' files, case-insensitive.
    Returns a list of full file paths.
    """
    found_readmes = []
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return found_readmes

    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower() == "readme.md":
                full_path = os.path.join(root, f)
                found_readmes.append(full_path)
    return found_readmes

def generate_markdown_links(paths):
    """
    Convert each README file path to a full GitHub URL, 
    with the parent folder as the link text, and append today's date.
    """
    md_lines = []
    # Get today's date in YYYY-MM-DD format
    today_str = datetime.now().strftime("%m-%d-%Y")

    for p in sorted(paths):
        # The folder name becomes the link text
        folder_name = os.path.basename(os.path.dirname(p))

        # Relative path from the current working directory
        rel_path = os.path.relpath(p, ".")
        # Replace backslashes with forward slashes
        forward_slash_path = rel_path.replace("\\", "/")
        # URL-encode to handle spaces, etc.
        encoded_path = urllib.parse.quote(forward_slash_path)

        # Combine with base URL, e.g.:
        # https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main/Resources/...
        final_url = f"{GITHUB_BASE_URL}/{encoded_path}"

        # Format: - [FolderName](full_url) - YYYY-MM-DD
        md_lines.append(f"- [{folder_name}]({final_url}) – {today_str}")

    return "\n".join(md_lines)

def read_file(filepath):
    """Return the text content of a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath, content):
    """Write text content to a file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def insert_into_readme(readme_content, insert_text):
    """
    Insert `insert_text` immediately after the header line "## 🔍 Latest Blog Posts".
    """
    pattern = rf"({LATEST_SECTION_HEADER}\s*\n+)"
    replacement = rf"\1{insert_text}\n\n"
    updated = re.sub(pattern, replacement, readme_content)
    return updated

def configure_git():
    """Configure Git user name and email if not already set."""
    try:
        # Check if user.name is set
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            subprocess.run(
                ["git", "config", "user.name", "Your Name"],
                check=True
            )
            print("Configured git user.name.")
        
        # Check if user.email is set
        result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            subprocess.run(
                ["git", "config", "user.email", "you@example.com"],
                check=True
            )
            print("Configured git user.email.")
    except subprocess.CalledProcessError as e:
        print("Failed to configure Git user information:")
        print(e.stderr)
        exit(1)


def main():
    # 0. Configure Git user
    configure_git()
    
    # 1. Collect all subdirectory READMEs
    readme_paths = get_writeup_readmes(WRITEUPS_DIR)
    if not readme_paths:
        print(f"No 'readme.md' files found under '{WRITEUPS_DIR}'. Exiting.")
        return

    # 2. Generate new markdown links for these READMEs
    new_md_content = generate_markdown_links(readme_paths)

    # 3. Read the top-level README.md
    if not os.path.exists(README_PATH):
        print(f"Could not find '{README_PATH}' in the current directory. Exiting.")
        return
    original_readme = read_file(README_PATH)

    # 4. Insert or update the "Latest Blog Posts" section
    updated_readme = insert_into_readme(original_readme, new_md_content)

    # 5. If changes were made, write them and commit
    if updated_readme != original_readme:
        write_file(README_PATH, updated_readme)
        print("README updated with new entries. Committing changes...")

        subprocess.run(["git", "add", README_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "🟢 New Write-up Added!"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    else:
        print("No changes detected in README.md.")

if __name__ == "__main__":
    main()
