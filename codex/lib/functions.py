from .templates import *
import os
import shutil
import subprocess
import re

def create(*directory, outdir: str = 'docs') -> None:
    """
    
    """
    assert isinstance(directory, tuple), "directory must be a tuple"
    if os.path.exists(outdir):
        print(f"Output directory '{outdir}' already exists, rebuilding...")
        shutil.rmtree(outdir)
    if len(directory) == 0:
        raise ValueError("No directory provided")
    if len(directory) > 1:
        raise ValueError("Multiple directories provided")
    _directory = directory[0]
    os.makedirs(source_dir := os.path.join(outdir, "source"), exist_ok = True)
    _create_conf(source_dir, outdir)
    _create_custom_css(source_dir)
    _create_index(source_dir, outdir)
    _build_doc(_directory, source_dir)
    _build_website(source_dir, outdir)
    return


def update(*directory,) -> None:
    """
    
    """
    if len(directory) == 0:
        raise ValueError("No directory provided")
    if len(directory) > 1:
        raise ValueError("Multiple directories provided")
    _directory: str = directory[0]
    assert os.path.exists(_directory), f"Directory '{_directory}' does not exist"
    print(f"Updating documentation in directory '{_directory}'")
    subprocess.run(f"sphinx-build -b html -a {os.path.abspath(_directory.replace("_build/html", ""))} docs/_build/html".split(" "))
    return


def delete(*directory) -> None:
    _directory = directory[0]
    assert os.path.exists(_directory), f"Directory '{_directory}' does not exist"
    shutil.rmtree(_directory)
    print(f"Deleted directory '{_directory}'")
    return


def deploy(*directory, port: str = '8000') -> None:
    """
    
    """
    if len(directory) == 0:
        raise ValueError("No directory provided")
    if len(directory) > 1:
        raise ValueError("Multiple directories provided")
    _directory = os.path.join(directory[0], "_build", "html")
    assert os.path.exists(_directory), f"Directory '{_directory}' does not exist"
    server_instance = f"python -m http.server {port} -d {_directory} -b localhost"
    subprocess.run(server_instance.split(" "))
    return


def pack() -> None:
    print("Executing 'pack' command")


def unpack() -> None:
    print("Executing 'unpack' command")


def build() -> None:
    """Docker image"""
    print("Executing 'build' command")


def _create_conf(source_dir: str , outdir: str) -> None:
    conf_file_path = os.path.join(source_dir, "conf.py")
    if os.path.exists(conf_file_path):
        print("conf.py already exists at:", conf_file_path)
        return
    with open(conf_file_path, "w", encoding = "utf-8") as f:
        f.write(SPHINX_CONFIG_TEMPLATE)
    shutil.copy2(conf_file_path, outdir + "/conf.py")
    print("Created conf.py at:", conf_file_path, "and copied to:", outdir + "/conf.py")
    return


def _create_custom_css(source_dir):
    static_dir = os.path.join(source_dir, "_static")
    os.makedirs(static_dir, exist_ok=True)
    custom_css_path = os.path.join(static_dir, "custom.css")
    if not os.path.exists(custom_css_path):
        with open(custom_css_path, "w", encoding = "utf-8") as f:
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
                title = _extract_title(full_path)
                documents.append((section, rel_path, title))
                print("Found Markdown for index:", rel_path, "with section", section)

    #* Sort based on the extracted section numbers (numeric and hierarchical order)
    documents.sort(key = lambda x: x[0])
    index_file = os.path.join(source_dir, "documents_index.rst")
    with open(index_file, "w", encoding = "utf-8") as f:
        f.write("Documents\n")
        f.write("=========\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 6\n\n")
        for section, path, title in documents:
            # Remove file extension — Sphinx toctree entries must be extensionless
            path_no_ext = os.path.splitext(path)[0]
            # Use explicit title so Sphinx doesn't need to parse the document for one
            f.write(f"   {title} <{path_no_ext}>\n")
    print(f"Markdown index generated at: {index_file}")

    #* Link associated documents to API pages ---
    _link_docs_to_api(api_output_dir, documents_target_dir, source_dir)
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


def _create_index(source_dir: str, outdir: str) -> None:
    """
    Create a minimal index.rst file (the master document) in the source directory.
    If index.rst already exists, it won't be overwritten.
    """
    index_file = os.path.join(source_dir, "index.rst")
    if os.path.exists(index_file):
        print("index.rst already exists at:", index_file)
        return
    with open(index_file, "w", encoding = "utf-8") as f:
        f.write(INDEX)
    shutil.copy2(index_file, outdir + "/index.rst")
    print("Created index.rst at:", index_file)
    return


def _link_docs_to_api(api_output_dir, documents_dir, source_dir):
    """
    Post-process API .rst files generated by sphinx-apidoc to append links
    to associated Markdown documents from the same source folder.

    Mapping logic:
      - The top-level package .rst (e.g. mypackage.rst) maps to documents/
      - A subpackage .rst (e.g. mypackage.sub.rst) maps to documents/sub/
    """

    # Build a mapping: relative folder -> list of (title, sphinx_path)
    folder_docs = {}
    for dirpath, _, files in os.walk(documents_dir):
        for file in files:
            if not file.endswith(".md"):
                continue
            full_path = os.path.join(dirpath, file)
            rel_folder = os.path.relpath(dirpath, documents_dir)
            title = _extract_title(full_path)
            # Sphinx path relative to source_dir, without extension
            sphinx_path = os.path.splitext(
                os.path.relpath(full_path, source_dir)
            )[0]
            folder_docs.setdefault(rel_folder, []).append((title, sphinx_path))

    # Process each API .rst file
    for rst_file in os.listdir(api_output_dir):
        if not rst_file.endswith(".rst"):
            continue
        rst_path = os.path.join(api_output_dir, rst_file)
        module_name = rst_file[:-4]  # strip .rst

        # Determine which document folder this API file maps to.
        # e.g. "mypackage" -> ".", "mypackage.configurators" -> "configurators"
        parts = module_name.split(".")
        if len(parts) <= 1:
            rel_folder = "."
        else:
            # Strip the top-level package name prefix
            rel_folder = os.path.join(*parts[1:])

        associated = folder_docs.get(rel_folder)
        if not associated:
            continue

        # Compute path from api/ to source_dir for cross-references
        api_to_source = os.path.relpath(source_dir, api_output_dir)

        # Prepend a "Related Documents" section to the top of the .rst file
        with open(rst_path, "r", encoding = "utf-8") as f:
            original = f.read()
        header = "Related Documents\n"
        header += "-" * 17 + "\n\n"
        for title, sphinx_path in sorted(associated):
            ref_path = os.path.join(api_to_source, sphinx_path)
            header += f"- :doc:`{title} <{ref_path}>`\n"
        header += "\n\n"
        with open(rst_path, "w", encoding = "utf-8") as f:
            # Insert after the first title + underline (first two non-empty lines)
            lines = original.split("\n")
            insert_idx = 0
            non_empty = 0
            for i, line in enumerate(lines):
                if line.strip():
                    non_empty += 1
                if non_empty == 2:
                    insert_idx = i + 1
                    break
            f.write("\n".join(lines[:insert_idx]) + "\n\n" + header + "\n".join(lines[insert_idx:]))
        print(f"Linked {len(associated)} document(s) to {rst_file}")


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


def _extract_title(file_path):
    """
    Extract the title from the first Markdown heading in the file.
    Falls back to the filename (without extension) if no heading is found.
    """
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.strip()
            match = re.match(r'^#+\s+(.+)$', line)
            if match:
                return match.group(1)
    return os.path.splitext(os.path.basename(file_path))[0]
