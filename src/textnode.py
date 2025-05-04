# src/textnode.py
from enum import Enum
# Import LeafNode from the htmlnode module
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    # ... (Existing TextNode class code) ...
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        tt_value = self.text_type.value if isinstance(self.text_type, Enum) else self.text_type
        return f"TextNode({self.text}, {tt_value}, {self.url})"

# --- Add the conversion function below ---

def text_node_to_html_node(text_node):
    """
    Converts a TextNode object into an HTMLNode (specifically a LeafNode)
    based on the TextNode's type.

    Args:
        text_node (TextNode): The TextNode to convert.

    Returns:
        LeafNode: The corresponding LeafNode representation.

    Raises:
        Exception: If the text_node has an invalid or unsupported text_type.
        # Consider using ValueError for more specific error handling
    """
    if not isinstance(text_node, TextNode):
         raise TypeError(f"Expected a TextNode object, but got {type(text_node)}")

    tt = text_node.text_type

    if tt == TextType.TEXT:
        # LeafNode constructor: value, tag=None, props=None
        return LeafNode(text_node.text) # tag defaults to None
    elif tt == TextType.BOLD:
        return LeafNode(text_node.text, "b")
    elif tt == TextType.ITALIC:
        return LeafNode(text_node.text, "i")
    elif tt == TextType.CODE:
        return LeafNode(text_node.text, "code")
    elif tt == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Invalid TextNode: Link type requires a URL.")
        # LeafNode constructor: value, tag, props
        return LeafNode(text_node.text, "a", {"href": text_node.url})
    elif tt == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Invalid TextNode: Image type requires a URL (src).")
        if text_node.text is None: # Alt text is technically optional but good practice
             raise ValueError("Invalid TextNode: Image type requires text (alt text).")
        # LeafNode constructor: value="", tag="img", props={...}
        return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
    else:
        # Handle unknown types
        raise ValueError(f"Unsupported text type: {text_node.text_type}")