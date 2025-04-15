from .templates import *
import os
import shutil
import subprocess
import re

def create(*directory, outdir: str = 'docs') -> None:
    """asdasdsdasd"""
    assert isinstance(directory, tuple), "directory must be a tuple"
    if len(directory) == 0:
        raise ValueError("No directory provided")
    if len(directory) > 1:
        raise ValueError("Multiple directories provided")
    _directory = directory[0]
    os.makedirs(source_dir := os.path.join(outdir, "source"), exist_ok = True)
    _create_conf(source_dir)
    _create_custom_css(source_dir)
    _create_index(source_dir)
    _build_doc(_directory, source_dir)
    _build_website(source_dir, outdir)
    return


def update() -> None:
    print("Executing 'update' command")


def delete() -> None:
    print("Executing 'delete' command")


def deploy(*directory, port: str = '8000') -> None:
    python_server = f"python -m http.server {port}"
    if len(directory) == 0:
        raise ValueError("No directory provided")
    if len(directory) > 1:
        raise ValueError("Multiple directories provided")
    _directory = os.path.join(directory[0], "_build", "html")
    print(f"Serving directory '{_directory}' on port {port} using Python HTTP server.")
    print("Executing command:", python_server)
    subprocess.run(python_server.split(" "), cwd = _directory)
    return
    


def pack() -> None:
    print("Executing 'pack' command")


def unpack() -> None:
    print("Executing 'unpack' command")


def build() -> None:
    print("Executing 'build' command")


def _create_conf(source_dir: str) -> None:
    conf_file_path = os.path.join(source_dir, "conf.py")
    if os.path.exists(conf_file_path):
        print("conf.py already exists at:", conf_file_path)
        return
    with open(conf_file_path, "w", encoding = "utf-8") as f:
        f.write(SPHINX_CONFIG_TEMPLATE)
    print("Created conf.py at:", conf_file_path)
    return


def _create_custom_css(source_dir):
    static_dir = os.path.join(source_dir, "_static")
    os.makedirs(static_dir, exist_ok=True)
    custom_css_path = os.path.join(static_dir, "custom.css")
    if not os.path.exists(custom_css_path):
        with open(custom_css_path, "w", encoding="utf-8") as f:
            f.write(CUSTOM_CSS_TEMPLATE)
        print("Created custom.css at:", custom_css_path)
    else:
        print("custom.css already exists at:", custom_css_path)
    return


def _build_doc(python_dir, source_dir):
    """
    Automate Sphinx documentation setup:
    1. Generate API documentation (.rst files) using sphinx-apidoc.
        These will be placed in source_dir/api.
    2. Recursively search for any Markdown (.md) file within python_dir,
        copy them into source_dir/documents preserving their relative path.
    3. Generate an index file (documents_index.rst) in source_dir that
        builds a toctree of all copied Markdown files, sorted based on section numbers.
    """
    #* Generate API documentation using sphinx-apidoc ---
    api_output_dir = os.path.join(source_dir, "api")
    os.makedirs(api_output_dir, exist_ok = True)
    try:
        subprocess.run(["sphinx-apidoc", "-o", api_output_dir, python_dir, '-M', '-d' '10'], check = True)
        print(f"API documentation generated in: {api_output_dir}")
    except subprocess.CalledProcessError as e:
        print("Error generating API docs with sphinx-apidoc:", e)
        return

    #* Copy all Markdown files from the project ---
    documents_target_dir = os.path.join(source_dir, "documents")
    os.makedirs(documents_target_dir, exist_ok=True)
    md_found = False
    for root, _, files in os.walk(python_dir):
        for file in files:
            if file.endswith(".md"):
                md_found = True
                source_file = os.path.join(root, file)
                rel_dir = os.path.relpath(root, python_dir)
                target_dir = os.path.join(documents_target_dir, rel_dir)
                os.makedirs(target_dir, exist_ok=True)
                dest_file = os.path.join(target_dir, file)
                shutil.copy2(source_file, dest_file)
                print(f"Copied Markdown file: {source_file} -> {dest_file}")
    if not md_found:
        print("No Markdown files found in", python_dir)

    #* Generate an index file for the Markdown documents ---
    documents = []
    for dirpath, _, files in os.walk(documents_target_dir):
        for file in files:
            if file.endswith(".md"):
                # Compute the path relative to source_dir so Sphinx can locate it.
                rel_path = os.path.relpath(os.path.join(dirpath, file), source_dir)
                full_path = os.path.join(source_dir, rel_path)
                section = _extract_section_number(full_path)
                documents.append((section, rel_path))
                print("Found Markdown for index:", rel_path, "with section", section)

    #* Sort based on the extracted section numbers (numeric and hierarchical order)
    documents.sort(key = lambda x: x[0])
    index_file = os.path.join(source_dir, "documents_index.rst")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("Documents\n")
        f.write("=========\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 6\n\n")
        for section, path in documents:
            f.write(f"   {path}\n")
    print(f"Markdown index generated at: {index_file}")
    return


def _build_website(source_dir, docs_dir, output_dir = None):
    """
    Build the Sphinx website (HTML) using source_dir as the source.
    The HTML output is placed in docs_dir/_build/html by default.
    """
    if output_dir is None:
        output_dir = os.path.join(docs_dir, "_build", "html")
    os.makedirs(output_dir, exist_ok=True)
    try:
        subprocess.run(["sphinx-build", "-b", "html", source_dir, output_dir], check=True)
        print(f"Website built successfully at: {output_dir}")
    except subprocess.CalledProcessError as e:
        print("Error building website:", e)
    return


def _create_index(source_dir):
    """
    Create a minimal index.rst file (the master document) in the source directory.
    If index.rst already exists, it won't be overwritten.
    """
    index_file = os.path.join(source_dir, "index.rst")
    if os.path.exists(index_file):
        print("index.rst already exists at:", index_file)
        return
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(INDEX)
    print("Created index.rst at:", index_file)
    return


def _extract_section_number(file_path):
    """
    Extract the section number from the first header in the Markdown file.
    It looks for a pattern like "# 1.0" or "# 1.1.2" and converts it into a tuple of integers.
    If no header is found, returns a tuple with a high value so the file sorts last.
    """
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.strip()
            # Look for a header starting with '#' followed by a section number (e.g., 1.0, 1.1, 2.0, etc.)
            match = re.match(r'#\s*(\d+(?:\.\d+)+)', line)
            if match:
                section_str = match.group(1)
                # Convert section string to a tuple of integers (e.g., "1.10" -> (1, 10))
                section_tuple = tuple(map(int, section_str.split('.')))
                return section_tuple
    return (float('inf'),)  # if no section is found, sort this file last
