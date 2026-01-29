import os

# --- CONFIGURATION ---
# Only include these file extensions
TARGET_EXTENSIONS = {'.evc', '.bdy'}
# Folders to completely ignore
SKIP_DIRS = {'.git', '.github', 'tools', 'backups'}
# Number of columns for the table
COLUMNS = 3

def create_progress_bar(percent, width=20):
    """Creates a visual progress bar using unicode blocks."""
    filled_chars = int(percent / (100 / width))
    bar = "█" * filled_chars + "░" * (width - filled_chars)
    return f"| `{bar}` {percent}% |"

def generate_markdown_checklist():
    all_files_found = []
   
    # 1. Gather all matching files
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if any(f.endswith(ext) for ext in TARGET_EXTENSIONS):
                all_files_found.append(os.path.join(root, f))

    if not all_files_found:
        print("No matching files found. Check your TARGET_EXTENSIONS!")
        return

    # 2. Build the Markdown
    output = "## Translation Progress\n\n"
   
    # Placeholder Progress Bar (You can update the 0% manually in the README)
    output += "Project Completion:\n"
    output += f"{create_progress_bar(0)}\n\n"
    output += "---\n\n### File Inventory\n\n"

    # 3. Group files by folder for the dropdowns
    grouped_files = {}
    for f_path in all_files_found:
        folder = os.path.dirname(f_path) if os.path.dirname(f_path) != '' else "Root"
        if folder not in grouped_files:
            grouped_files[folder] = []
        grouped_files[folder].append(os.path.basename(f_path))

    for folder, files in grouped_files.items():
        files.sort()
        output += f"<details>\n<summary><b>📁 {folder} ({len(files)} files)</b></summary>\n\n"
       
        # Table Header
        output += "| " + " | ".join(["File"] * COLUMNS) + " |\n"
        output += "| " + " | ".join([":---"] * COLUMNS) + " |\n"
       
        # Table Rows
        for i in range(0, len(files), COLUMNS):
            row_files = files[i:i + COLUMNS]
            row_items = [f"- [ ] `{f}`" for f in row_files]
            while len(row_items) < COLUMNS:
                row_items.append(" ")
            output += "| " + " | ".join(row_items) + " |\n"
       
        output += "\n</details>\n\n"

    with open("file_tracker.md", "w", encoding="utf-8") as f:
        f.write(output)
   
    print(f"Found {len(all_files_found)} files. Checklist generated in 'file_tracker.md'")

if __name__ == "__main__":
    generate_markdown_checklist()