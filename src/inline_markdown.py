import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNodes of type TEXT based on a given delimiter.

    Takes a list of TextNodes, a delimiter string (e.g., "`", "**", "_"),
    and a TextType enum member (e.g., TextType.CODE, TextType.BOLD).

    Returns a new list of TextNodes where nodes of type TEXT have been
    split. Text between delimiters gets the specified `text_type`, while
    text outside remains TEXT. Non-TEXT nodes are passed through unchanged.

    Args:
        old_nodes (list[TextNode]): The list of nodes to process.
        delimiter (str): The delimiter string to split by (e.g., "`").
        text_type (TextType): The type to assign to text between delimiters.

    Returns:
        list[TextNode]: A new list with nodes potentially split.

    Raises:
        ValueError: If an unmatched delimiter is found within a TEXT node.
    """
    new_nodes = []
    for old_node in old_nodes:
        # If the node is not plain text, add it as is and continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # If the node is text, split it
        split_parts = old_node.text.split(delimiter)

        # Check for valid splitting (must have odd number of parts for matched pairs)
        # Example: "text `code` text" -> ["text ", "code", " text"] (3 parts - OK)
        # Example: "text `code" -> ["text ", "code"] (2 parts - Error)
        if len(split_parts) % 2 == 0:
             # Check if delimiter was actually present, otherwise it's not an error
             # Example: "plain text".split("`") -> ["plain text"] (1 part - OK)
             if len(split_parts) > 1: # Only raise error if splitting actually occurred
                raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' in text: '{old_node.text}'")
             else: # No delimiter found, just add the original node
                 new_nodes.append(old_node)
                 continue # Skip further processing for this node


        # Process the split parts
        for i, part in enumerate(split_parts):
            # Skip empty parts which can occur if delimiters are adjacent
            # or at the beginning/end of the string
            if not part:
                continue

            # Parts outside the delimiter (even indices) remain TEXT type
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            # Parts inside the delimiter (odd indices) get the new text_type
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    """
    Extracts all Markdown images from a given text.

    Args:
        text (str): The raw text containing Markdown.

    Returns:
        list[tuple[str, str]]: A list of tuples, where each tuple contains
                                the alt text and the URL of an image.
                                Example: [("alt text", "url.png"), ...]
    """
    # Regex Breakdown:
    # !             - Literal exclamation mark
    # \[            - Literal opening square bracket
    # ([^\[\]]*)   - Capture group 1: Zero or more characters that are NOT '[' or ']' (alt text)
    # \]            - Literal closing square bracket
    # \(            - Literal opening parenthesis
    # ([^\(\)]*)   - Capture group 2: Zero or more characters that are NOT '(' or ')' (URL)
    # \)            - Literal closing parenthesis
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    # matches will be a list of tuples, e.g., [('alt1', 'url1'), ('alt2', 'url2')]
    return matches

def extract_markdown_links(text):
    """
    Extracts all Markdown links (not images) from a given text.

    Args:
        text (str): The raw text containing Markdown.

    Returns:
        list[tuple[str, str]]: A list of tuples, where each tuple contains
                                the anchor text and the URL of a link.
                                Example: [("anchor text", "url.com"), ...]
    """
    # Regex Breakdown:
    # (?<!!)        - Negative Lookbehind: Asserts that the preceding character is NOT '!'
    #               - (Ensures we don't match images)
    # \[            - Literal opening square bracket
    # ([^\[\]]*)   - Capture group 1: Zero or more characters that are NOT '[' or ']' (anchor text)
    # \]            - Literal closing square bracket
    # \(            - Literal opening parenthesis
    # ([^\(\)]*)   - Capture group 2: Zero or more characters that are NOT '(' or ')' (URL)
    # \)            - Literal closing parenthesis
    regex = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    # matches will be a list of tuples, e.g., [('anchor1', 'url1'), ('anchor2', 'url2')]
    return matches

def split_nodes_image(old_nodes):
    """
    Splits TextNodes of type TEXT based on Markdown image syntax.

    Takes a list of TextNodes and returns a new list where TEXT nodes
    containing image markdown (![alt](url)) are split into separate
    TEXT, IMAGE, and TEXT nodes. Non-TEXT nodes are passed through.

    Args:
        old_nodes (list[TextNode]): The list of nodes to process.

    Returns:
        list[TextNode]: A new list with nodes potentially split by images.
    """
    new_nodes = []
    for old_node in old_nodes:
        # If not a TEXT node, pass it through unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        # Extract all images from the current node's text
        images = extract_markdown_images(original_text)

        # If no images found, add the original node and continue
        if not images:
            if original_text: # Only add if the original text wasn't empty
                new_nodes.append(old_node)
            continue

        # Start with the full text of the node
        text_to_process = original_text
        for alt, url in images:
            # Construct the full markdown string for the current image
            markdown_image = f"![{alt}]({url})"
            # Split the text based on the first occurrence of this image
            sections = text_to_process.split(markdown_image, 1)

            # Handle potential errors or unexpected splitting
            if len(sections) != 2:
                # This might happen if the text somehow doesn't contain the extracted image
                # (shouldn't happen with correct extraction/splitting)
                # Or if the text *was* the image markdown itself. Handle gracefully.
                 if text_to_process == markdown_image: # If the whole segment was the image
                     new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                     text_to_process = "" # Nothing left
                     break # Exit loop for this old_node
                 else:
                    # Treat the rest as plain text if split fails unexpectedly
                    if text_to_process:
                         new_nodes.append(TextNode(text_to_process, TextType.TEXT))
                    text_to_process = "" # Mark as processed
                    break # Avoid infinite loop

            # Text before the image
            text_before = sections[0]
            # Text after the image (becomes the text_to_process for the next iteration)
            text_after = sections[1]

            # Add the text node for the part before the image, if it's not empty
            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))

            # Add the image node itself
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            # Update the text to process for the next image
            text_to_process = text_after

        # After iterating through all images, add any remaining text
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits TextNodes of type TEXT based on Markdown link syntax.

    Takes a list of TextNodes and returns a new list where TEXT nodes
    containing link markdown ([anchor](url)) are split into separate
    TEXT, LINK, and TEXT nodes. Non-TEXT nodes are passed through.

    Args:
        old_nodes (list[TextNode]): The list of nodes to process.

    Returns:
        list[TextNode]: A new list with nodes potentially split by links.
    """
    new_nodes = []
    for old_node in old_nodes:
        # If not a TEXT node, pass it through unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        # Extract all links from the current node's text
        links = extract_markdown_links(original_text)

        # If no links found, add the original node and continue
        if not links:
            if original_text: # Only add if not empty
                new_nodes.append(old_node)
            continue

        # Start with the full text of the node
        text_to_process = original_text
        for anchor, url in links:
            # Construct the full markdown string for the current link
            markdown_link = f"[{anchor}]({url})"
            # Split the text based on the first occurrence of this link
            sections = text_to_process.split(markdown_link, 1)

            # Handle potential errors or unexpected splitting
            if len(sections) != 2:
                 if text_to_process == markdown_link: # If the whole segment was the link
                     new_nodes.append(TextNode(anchor, TextType.LINK, url))
                     text_to_process = ""
                     break
                 else:
                    if text_to_process:
                         new_nodes.append(TextNode(text_to_process, TextType.TEXT))
                    text_to_process = ""
                    break

            # Text before the link
            text_before = sections[0]
            # Text after the link
            text_after = sections[1]

            # Add the text node for the part before the link, if it's not empty
            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))

            # Add the link node itself
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            # Update the text to process for the next link
            text_to_process = text_after

        # After iterating through all links, add any remaining text
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    """
    Converts a raw string containing Markdown inline syntax into a list
    of TextNode objects.

    Handles images, links, bold, italic, and code elements.

    Args:
        text (str): The raw string to convert.

    Returns:
        list[TextNode]: A list of TextNodes representing the parsed text.
    """
    # Start with a single node representing the whole text
    initial_node = TextNode(text, TextType.TEXT)
    nodes = [initial_node]

    # Apply splitting functions in sequence. Order matters!
    # Images and Links first, as their syntax is more complex.
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # Then apply delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) # Use underscore for italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Filter out any empty text nodes that might have been created
    # Although the split functions aim to avoid this, a final check is safe.
    # final_nodes = [node for node in nodes if node.text] # Optional cleanup

    return nodes # Return the processed list