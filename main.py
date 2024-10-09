import os
import time
import datetime
import subprocess
import platform
import re
from pathlib import Path

def get_markdown_files(directory):
    """Recursively get all markdown files in the given directory."""
    return list(Path(directory).rglob("*.md"))

def get_creation_date(file_path):
    """Get the creation date of the file."""
    # return datetime.datetime.fromtimestamp(os.path.getctime(file_path))
    system_platform = platform.system()
    
    if system_platform == 'Darwin':  # macOS
        # Use stat to get the creation time on macOS
        result = subprocess.run(['stat', '-f%B', file_path], stdout=subprocess.PIPE, text=True)
        creation_time = int(result.stdout.strip())
    elif system_platform == 'Linux':  # Linux
        # Use stat to get the birth time (creation time) on Linux, if supported
        result = subprocess.run(['stat', '-c%W', file_path], stdout=subprocess.PIPE, text=True)
        creation_time = int(result.stdout.strip())
        if creation_time == 0:
            raise OSError("File system does not support birth time (creation time).")
    else:
        raise OSError(f"Unsupported platform: {system_platform}")
    return creation_time

def get_title(file_path):
    """Extract the title from the markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Look for a # heading or use the filename if not found
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
        return file_path.stem

def collect_file_info(directories):
    """Collect information about markdown files in the given directories."""
    all_files = []
    for directory in directories:
        files = get_markdown_files(directory)
        for file in files:
            all_files.append({
                'path': file,
                'created': get_creation_date(file),
                'title': get_title(file)
            })
    return all_files

def write_markdown_list(file_info, output_file):
    """Write the collected file information into a markdown file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Markdown Files List\n\n")
        for file in sorted(file_info, key=lambda x: x['created'], reverse=True):
            f.write(f"- [{file['title']}]({file['path']})\n")
            f.write(f"  - Created: {time.ctime(file['created'])}\n")

def main():
    directories = ["./docs/highthoughts/", "./docs/zettels/"]  # Add your directories here
    output_file = "./docs/dex/index.md"

    file_info = collect_file_info(directories)
    write_markdown_list(file_info, output_file)
    print(f"Markdown file list has been written to {output_file}")

if __name__ == "__main__":
    main()