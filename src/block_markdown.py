# src/block_markdown.py
from enum import Enum
import re # For heading regex check
# Import node types and text processing functions
from htmlnode import ParentNode, LeafNode, HTMLNode # Added HTMLNode for type hints potentially
from textnode import TextNode, TextType # Added TextNode/Type for text_to_children
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node # Function to convert TextNode -> LeafNode
# --- Define BlockType Enum ---
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
    
    
def markdown_to_blocks(markdown):
    """
    Splits a raw Markdown string into a list of block strings.

    Blocks are separated by one or more blank lines. Leading/trailing
    whitespace is stripped from each block, and empty blocks resulting
    from multiple blank lines are removed.

    Args:
        markdown (str): The raw Markdown text.

    Returns:
        list[str]: A list of block strings.
    """
    # Split the markdown text by sequences of two or more newlines.
    # This naturally handles varying numbers of blank lines between blocks.
    raw_blocks = markdown.split('\n\n')

    # Filter out empty blocks and strip whitespace from the others
    filtered_blocks = []
    for block in raw_blocks:
        if not block: # Skip if the block is empty (e.g., from multiple \n\n)
            continue
        # Strip leading/trailing whitespace from the content of the block
        stripped_block = block.strip()
        # Ensure the block wasn't just whitespace before adding
        if stripped_block:
            filtered_blocks.append(stripped_block)

    return filtered_blocks

def block_to_block_type(block):
    """
    Determines the type of a single Markdown block.

    Assumes leading/trailing whitespace has already been stripped.

    Args:
        block (str): A single block of Markdown text.

    Returns:
        BlockType: The determined type of the block.
    """
    lines = block.split('\n')

    # 1. Check for Heading (1-6 '#' followed by space)
    # Regex: ^#{1,6} .* matches start of string, 1-6 hashes, a space, then anything
    # Using re.match ensures it's at the beginning of the first line only.
    if re.match(r"^#{1,6} ", lines[0]): # Check only the first line for heading marker
         # Ensure it's just the marker and space, not the whole block starting with hashes
         # The regex match handles this implicitly as it requires the space.
        return BlockType.HEADING

    # 2. Check for Code Block (starts and ends with ```)
    # Needs at least one line inside potentially, but start/end is key.
    # The block should start and end with ``` and can have any content in between.
    # We also check if the block is at least 6 characters long to ensure it's not just ```.
    # This is a simple check, but it assumes the block is not empty.
    # If the block is empty, it won't match this condition.   
    if len(block) > 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE


    # 3. Check for Quote Block (every line starts with '>')
    all_lines_quote = True
    if not lines: # Handle empty block case if it somehow gets here
        all_lines_quote = False
    for line in lines:
        if not line.startswith(">"):
            all_lines_quote = False
            break
    if all_lines_quote:
        return BlockType.QUOTE

    # 4. Check for Unordered List (every line starts with '* ' or '- ')
    all_lines_ul = True
    if not lines:
        all_lines_ul = False
    for line in lines:
        # Prompt says '-' but '*' is common, let's allow both for robustness
        if not (line.startswith("* ") or line.startswith("- ")):
            all_lines_ul = False
            break
    if all_lines_ul:
        return BlockType.UNORDERED_LIST

    # 5. Check for Ordered List (every line starts '1. ', '2. ', etc.)
    all_lines_ol = True
    expected_number = 1
    if not lines:
        all_lines_ol = False
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            all_lines_ol = False
            break
        expected_number += 1
    if all_lines_ol:
        return BlockType.ORDERED_LIST

    # 6. If none of the above, it's a Paragraph
    return BlockType.PARAGRAPH

def text_to_children(text):
    """Converts inline markdown text to a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

# --- Helper functions for converting specific block types to HTMLNodes ---

def paragraph_block_to_html_node(block):
    """Converts a paragraph block to a <p> HTMLNode."""
    # Replace internal newlines with spaces
    content = block.replace('\n', ' ')

    children = text_to_children(content)

    return ParentNode("p", children)

def heading_block_to_html_node(block):
    """Converts a heading block to an <h1>-<h6> HTMLNode."""
    lines = block.split('\n')
    first_line = lines[0] # Work only with the first line

    level = 0
    # Correctly count '#' characters
    while level < len(first_line) and first_line[level] == '#':
        level += 1

    # Determine content start index (after '# ' characters)
    # Check for the space after hashes, assuming block_to_block_type validated it
    content_start_index = level + 1
    if level >= len(first_line) or first_line[level] != ' ':
         # Defensive check - should not happen if block type check is robust
         # If it does, treat the whole line after hashes as content maybe?
         # Or stick to the assumption based on block_to_block_type:
         content_start_index = level + 1 # Assume space exists

    # Extract content ONLY from the first line after the marker
    content = first_line[content_start_index:].strip()
    children = text_to_children(content) # Process only heading text for inline elements
    tag = f"h{level}"
    return ParentNode(tag, children)

def code_block_to_html_node(block):
    """Converts a code block to a <pre><code> HTMLNode structure."""
    # Content is between ``` markers, stripping leading/trailing newlines if present
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block format") # Should be caught earlier ideally
    content = block[3:-3].strip('\n') # Remove fences and surrounding newlines
    # No inline processing for code content
    # Create LeafNode for the content itself inside a <code> tag
    code_content_node = LeafNode(content, "code")
    # Wrap the <code> node in a <pre> node
    return ParentNode("pre", [code_content_node])

def quote_block_to_html_node(block):
    """Converts a quote block to a <blockquote> HTMLNode."""
    lines = block.split('\n')
    # Remove '>' and optional leading space from each line
    content_lines = [line.lstrip('> ').lstrip('>') for line in lines]
    content = "\n".join(content_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_list_block_to_html_node(block):
    """Converts an unordered list block to a <ul> HTMLNode."""
    list_items = []
    lines = block.split('\n')
    for line in lines:
        if not line: continue # Skip empty lines if any
        # Remove '- ' or '* ' marker
        content = line[2:] # Assumes marker is always 2 chars '* ' or '- '
        children = text_to_children(content)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)

def ordered_list_block_to_html_node(block):
    """Converts an ordered list block to an <ol> HTMLNode."""
    list_items = []
    lines = block.split('\n')
    for line in lines:
        if not line: continue # Skip empty lines if any
        # Find the first space after the dot 'N. '
        first_space_index = line.find(' ')
        if first_space_index == -1: continue # Malformed line? Skip.
        content = line[first_space_index + 1:]
        children = text_to_children(content)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


# --- Main Conversion Function ---

def markdown_to_html_node(markdown):
    """
    Converts a full Markdown document string into a single parent HTMLNode ('div').

    Args:
        markdown (str): The full Markdown document text.

    Returns:
        ParentNode: An HTMLNode (specifically a 'div' ParentNode) containing
                    the HTML representation of the document.
    """
    blocks = markdown_to_blocks(markdown)
    children_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        node = None
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_block_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_block_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_block_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_block_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_block_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_block_to_html_node(block)
        else:
            # This should not happen if block_to_block_type is comprehensive
            raise ValueError(f"Unknown block type encountered: {block_type}")

        if node:
            children_nodes.append(node)

    # Wrap all block nodes in a single root 'div' node
    return ParentNode("div", children_nodes)

def extract_title(markdown):
    """
    Extracts the content of the first H1 heading ('# ') from Markdown text.

    Args:
        markdown (str): The Markdown text to parse.

    Returns:
        str: The text content of the H1 heading.

    Raises:
        ValueError: If no H1 heading is found in the Markdown.
    """
    lines = markdown.split('\n')
    for line in lines:
        stripped_line = line.strip() # Allow for leading whitespace before #
        if stripped_line.startswith('# '):
            # Found H1, return content after '# ' and strip whitespace
            return stripped_line[2:].strip()
    # If loop finishes without finding H1
    raise ValueError("Invalid Markdown: No H1 heading found.")