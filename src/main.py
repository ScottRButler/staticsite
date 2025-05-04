# src/main.py
import os
from block_markdown import markdown_to_html_node, extract_title

# --- Custom Recursive Removal ---
def remove_directory_recursive(dir_path):
    """Recursively removes a directory and all its contents."""
    if not os.path.exists(dir_path):
        # print(f"  Directory '{dir_path}' does not exist, nothing to remove.")
        return
    if not os.path.isdir(dir_path):
        print(f"  Error: '{dir_path}' is not a directory.")
        return

    # print(f"  Removing contents of directory: {dir_path}")
    try:
        items = os.listdir(dir_path)
        for item in items:
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path):
                # print(f"    Removing file: {item_path}")
                os.remove(item_path)
            elif os.path.isdir(item_path):
                remove_directory_recursive(item_path) # Recursive call

        # print(f"  Removing empty directory: {dir_path}")
        os.rmdir(dir_path)
    except OSError as e:
        print(f"  Error removing directory {dir_path}: {e}")


# --- Manual File Copy and Recursive Directory Copy ---
def copy_file_manual(src_file_path, dest_file_path):
    """Manually copies a single file using read/write."""
    # print(f"    Copying: {src_file_path} -> {dest_file_path}")
    try:
        with open(src_file_path, 'rb') as src_file, open(dest_file_path, 'wb') as dest_file:
            while True:
                chunk = src_file.read(4096)
                if not chunk:
                    break
                dest_file.write(chunk)
    except OSError as e:
        print(f"    Error copying file {src_file_path} to {dest_file_path}: {e}")


def copy_directory_recursive(src_path, dest_path):
    """
    Recursively copies contents from src_path to dest_path
    using only the 'os' module and manual file I/O.
    """
    if not os.path.exists(src_path):
        raise ValueError(f"Source directory not found: {src_path}")
    if not os.path.isdir(src_path):
         raise ValueError(f"Source path must be a directory: {src_path}")

    # Use makedirs which can create intermediate directories if needed
    # and doesn't error if the directory already exists.
    os.makedirs(dest_path, exist_ok=True)
    # print(f"Ensured destination directory exists: {dest_path}")

    items = os.listdir(src_path)
    for item in items:
        full_src_path = os.path.join(src_path, item)
        full_dest_path = os.path.join(dest_path, item)

        if os.path.isfile(full_src_path):
            copy_file_manual(full_src_path, full_dest_path)
        elif os.path.isdir(full_src_path):
            copy_directory_recursive(full_src_path, full_dest_path) # Recursive call

def generate_page(from_path, template_path, dest_path):
    """
    Generates an HTML page from a Markdown file using a template.

    Args:
        from_path (str): Path to the source Markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Path where the generated HTML file will be saved.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1. Read Markdown file
    try:
        with open(from_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown source file not found: {from_path}")
    except Exception as e:
        raise Exception(f"Error reading Markdown file {from_path}: {e}")

    # 2. Read Template file
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")
    except Exception as e:
        raise Exception(f"Error reading template file {template_path}: {e}")

    # 3. Convert Markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # 4. Extract Title
    try:
        title = extract_title(markdown_content)
    except ValueError as e:
        raise ValueError(f"Could not extract title from {from_path}: {e}")

    # 5. Replace placeholders
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # 6. Write the new HTML to dest_path
    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir: # Only create if path includes a directory
        os.makedirs(dest_dir, exist_ok=True)

    try:
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"  Successfully wrote page to {dest_path}")
    except Exception as e:
        raise Exception(f"Error writing HTML file to {dest_path}: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages from Markdown files in a source directory
    to a destination directory using a template.

    Args:
        dir_path_content (str): Path to the current content directory being processed.
        template_path (str): Path to the HTML template file.
        dest_dir_path (str): Path to the corresponding destination directory.
    """
    if not os.path.isdir(dir_path_content):
        print(f"Warning: Content path '{dir_path_content}' is not a directory. Skipping.")
        return

    # print(f"Processing directory: {dir_path_content} -> {dest_dir_path}")
    # Ensure destination directory exists for the current level
    os.makedirs(dest_dir_path, exist_ok=True)

    items = os.listdir(dir_path_content)
    for item in items:
        full_src_path = os.path.join(dir_path_content, item)
        full_dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(full_src_path):
            # Check if it's a Markdown file
            if item.lower().endswith(".md"):
                # Calculate destination HTML path
                base_name, _ = os.path.splitext(item)
                dest_html_path = os.path.join(dest_dir_path, f"{base_name}.html")
                try:
                    generate_page(full_src_path, template_path, dest_html_path)
                except Exception as e:
                    print(f"Error generating page for {full_src_path}: {e}")
            # else: Ignore non-markdown files in content dir
        elif os.path.isdir(full_src_path):
            # Recursively process subdirectory
            # Destination path for subdirectory is already calculated as full_dest_path
            generate_pages_recursive(full_src_path, template_path, full_dest_path)
        # else: Ignore other types


# --- Main Function ---
def main():
    print("Starting static site generation...")

    static_dir = "static"
    content_dir = "content"
    template_path = "template.html"
    public_dir = "public"

    # Clean public directory
    print(f"\nCleaning destination directory: {public_dir}...")
    remove_directory_recursive(public_dir)
    try:
        os.mkdir(public_dir)
        print(f"  Created empty directory: {public_dir}")
    except OSError as e:
        print(f"  Error creating directory {public_dir}: {e}")
        return

    # Copy static files
    print(f"\nCopying static files from {static_dir} to {public_dir}...")
    if os.path.exists(static_dir) and os.path.isdir(static_dir):
        copy_directory_recursive(static_dir, public_dir)
        print(f"  Finished copying static files.")
    else:
        print(f"  Warning: Static directory '{static_dir}' not found or is not a directory. Skipping copy.")

    # --- Generate content pages recursively ---
    print(f"\nGenerating content pages from {content_dir}...")
    try:
        # Call the new recursive function starting at the root content/public dirs
        generate_pages_recursive(
            content_dir,
            template_path,
            public_dir
        )
        print("  Finished generating content pages.")
    except Exception as e:
        print(f"\nError during page generation: {e}")
        return

    print("\nStatic site generation complete!")

# Call the main function when the script is run
if __name__ == "__main__":
    main()