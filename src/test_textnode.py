# src/test_textnode.py
import unittest
from enum import Enum

# Import necessary items
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode # We need LeafNode for comparison

class TestTextNode(unittest.TestCase):
    # --- Existing tests for TextNode equality ---
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        node = TextNode("Node text 1", TextType.TEXT)
        node2 = TextNode("Node text 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_different_type(self):
        node = TextNode("Same text", TextType.ITALIC)
        node2 = TextNode("Same text", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_neq_different_url(self):
        node = TextNode("Link node", TextType.LINK, "https://example.com")
        node2 = TextNode("Link node", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("Plain text", TextType.TEXT, None)
        node2 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Image node", TextType.IMAGE, "https://image.com/img.png")
        node2 = TextNode("Image node", TextType.IMAGE, "https://image.com/img.png")
        self.assertEqual(node, node2)

    def test_neq_other_object(self):
        node = TextNode("Some text", TextType.TEXT)
        other = "Just a string"
        self.assertNotEqual(node, other)

    # --- New tests for text_node_to_html_node ---

    def test_convert_text(self):
        """Tests conversion of TEXT type."""
        node = TextNode("Just raw text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        # Expected: LeafNode(value="Just raw text", tag=None)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Just raw text")
        self.assertIsNone(html_node.tag)
        self.assertIsNone(html_node.props)

    def test_convert_bold(self):
        """Tests conversion of BOLD type."""
        node = TextNode("Bold content", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        # Expected: LeafNode(value="Bold content", tag="b")
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Bold content")
        self.assertEqual(html_node.tag, "b")
        self.assertIsNone(html_node.props)

    def test_convert_italic(self):
        """Tests conversion of ITALIC type."""
        node = TextNode("Italicized", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        # Expected: LeafNode(value="Italicized", tag="i")
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Italicized")
        self.assertEqual(html_node.tag, "i")
        self.assertIsNone(html_node.props)

    def test_convert_code(self):
        """Tests conversion of CODE type."""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        # Expected: LeafNode(value="print('hello')", tag="code")
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.tag, "code")
        self.assertIsNone(html_node.props)

    def test_convert_link(self):
        """Tests conversion of LINK type."""
        url = "https://www.example.com"
        node = TextNode("Click Here", TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        # Expected: LeafNode(value="Click Here", tag="a", props={"href": url})
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Click Here")
        self.assertEqual(html_node.tag, "a")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props, {"href": url})

    def test_convert_image(self):
        """Tests conversion of IMAGE type."""
        img_url = "https://example.com/image.png"
        alt_text = "An example image"
        node = TextNode(alt_text, TextType.IMAGE, img_url)
        html_node = text_node_to_html_node(node)
        # Expected: LeafNode(value="", tag="img", props={"src": img_url, "alt": alt_text})
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "") # Image tag has no value
        self.assertEqual(html_node.tag, "img")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props, {"src": img_url, "alt": alt_text})

    def test_convert_invalid_type(self):
        """Tests that an invalid TextType raises an error."""
        # Create a TextNode with a type not in TextType (or simulate one)
        # We can directly assign an invalid string value for testing purposes if needed
        # Or create a fake enum member if that's easier
        class FakeTextType(Enum):
            FAKE = "fake"
        node = TextNode("Some text", FakeTextType.FAKE) # Use a type not handled
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        # Check the error message contains something useful
        self.assertIn("Unsupported text type", str(cm.exception))

    def test_convert_link_no_url(self):
        """Tests ValueError if LINK type has no URL."""
        node = TextNode("Link text", TextType.LINK, None)
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertIn("Link type requires a URL", str(cm.exception))

    def test_convert_image_no_url(self):
        """Tests ValueError if IMAGE type has no URL."""
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertIn("Image type requires a URL", str(cm.exception))

    def test_convert_image_no_alt(self):
        """Tests ValueError if IMAGE type has no text (alt text)."""
        node = TextNode(None, TextType.IMAGE, "http://example.com/img.jpg")
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertIn("Image type requires text (alt text)", str(cm.exception))

# Standard boilerplate to run tests if the script is executed directly
if __name__ == "__main__":
    unittest.main()