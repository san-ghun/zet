# Dexer: A markdown file list generator for Zettelkasten

The Python script, `dexer.py`, is designed to catalog markdown files from specified directories. Here's what it does:

1. Reads configuration (directories to scan and output file name) from a JSON file.
2. Recursively searches the specified directories for markdown (.md) files.
3. For each markdown file found, it:
   - Extracts the creation date
   - Attempts to parse the title (first heading or filename if no heading)
   - Records the file path
4. Compiles all this information into a list.
5. Generates a new markdown file that lists all found files, sorted by creation date (newest first).
6. Each entry in the output file includes the file's title, creation date, and path.

### Key features:

- Uses only Python standard library (no external dependencies)
- Configurable via an external JSON file
- Handles multiple directories
- Extracts useful metadata from each markdown file

This tool is particularly useful for creating an index or catalog of markdown files across multiple directories, which could be helpful for managing documentation, blog posts, or any collection of markdown-based content.

## Remarks

This script reads markdown files in a directory and generates a markdown file
listing all the files in the directory with their creation date and title.
The output file can be used as a Zettelkasten index.

#### Usage:

```sh
python dexer.py
or
python3 dexer.py
```

#### Requirements:

- Python 3 (no extra dependencies)

#### Configuration:

Add the following JSON object to config.json:

```json
{
  "directories": ["./docs/highthoughts/", "./docs/zettels/"],
  "output_file": "./docs/dex/index.md"
}
```

- Set the directories to the paths of the directories containing the markdown files.
- Set the output_file to the path of the output markdown file.

---

Author: [San-ghun](https://github.com/san-ghun)
License: MIT
