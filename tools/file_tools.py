import os


def read_file(path: str):
    """Read and return the contents of a text file."""
    if not os.path.exists(path):
        return f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Keep responses sane for large files
        if len(content) > 4000:
            return content[:4000] + "\n...[truncated]"
        return content
    except Exception as e:
        return f"Couldn't read file: {e}"


def write_file(path: str, content: str):
    """Write text content to a file (creates or overwrites)."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Saved to {path}."
    except Exception as e:
        return f"Couldn't write file: {e}"


def search_files(directory: str, keyword: str):
    """Search a directory for filenames containing a keyword."""
    if not os.path.isdir(directory):
        return f"Directory not found: {directory}"
    matches = []
    for root, _, files in os.walk(directory):
        for name in files:
            if keyword.lower() in name.lower():
                matches.append(os.path.join(root, name))
    if not matches:
        return f"No files matching '{keyword}' in {directory}."
    return "Found:\n" + "\n".join(matches[:20])


def register_file_tools(registry):
    registry.register(
        name="read_file",
        func=read_file,
        description="Read the text contents of a file at a given path.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Full path to the file."}
            },
            "required": ["path"],
        },
    )

    registry.register(
        name="write_file",
        func=write_file,
        description="Write text content to a file (creates or overwrites it).",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Full path to the file."},
                "content": {"type": "string", "description": "Text to write."},
            },
            "required": ["path", "content"],
        },
        sensitive=True,   # 🔐 writing changes disk -> confirm first
    )

    registry.register(
        name="search_files",
        func=search_files,
        description="Search a directory for files whose name contains a keyword.",
        parameters={
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Folder to search in."},
                "keyword": {"type": "string", "description": "Text to look for in filenames."},
            },
            "required": ["directory", "keyword"],
        },
    )