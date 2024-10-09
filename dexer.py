import os
import time
import subprocess
import platform
import re
import json
from pathlib import Path

def get_markdown_files(directory):
    """Recursively get all markdown files in the given directory."""
    return list(Path(directory).rglob("*.md"))

def get_creation_date(file_path):
    """Get the creation date of the file."""
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
                'path': file.as_posix(),
                'created': get_creation_date(file),
                'title': get_title(file)
            })
    return all_files

def parse_path(path: str) -> str:
    """Parse the path to remove the 'docs/' prefix and '.md' extension."""
    # Remove the 'docs/' prefix
    path = path.replace('docs/', '')
    
    # Remove '.md' extension
    path = path.replace('.md', '')
    
    # Ensure directory paths end with a slash
    if os.path.basename(path) == "README":
        path = os.path.dirname(path) + "/"
    
    return path

def write_markdown_list(file_info, output_file):
    """Write the collected file information into a markdown file."""
    link_prefix = "https://san-ghun.github.io/zet"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Index\n\n")
        for file in sorted(file_info, key=lambda x: x['created'], reverse=True):
            f.write(f"- [{file['title']}]({link_prefix}/{parse_path(file['path'])})\n")
            f.write(f"  - Created: {time.ctime(file['created'])}\n")

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def main():
    config = load_config('config.json')
    directories = config['directories']
    output_file = config['output_file']

    file_info = collect_file_info(directories)
    write_markdown_list(file_info, output_file)
    print(f"Markdown file list has been written to {output_file}")

if __name__ == "__main__":
    main()