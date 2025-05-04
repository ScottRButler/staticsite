import unittest
from htmlnode import LeafNode # Assuming LeafNode is in htmlnode.py

class TestLeafNode(unittest.TestCase):

    # Test case 1: Simple paragraph
    def test_to_html_p(self):
        """Tests rendering a simple paragraph tag."""
        # CORRECTED ORDER: value first, then tag
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Test case 2: Anchor tag with properties
    def test_to_html_a(self):
        """Tests rendering an anchor tag with href attribute."""
        # CORRECTED ORDER: value first, then tag, then props
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    # Test case 3: Raw text (no tag)
    def test_to_html_raw_text(self):
        """Tests rendering raw text when the tag is None."""
        # CORRECT ORDER: value first, tag is None (implicitly or explicitly)
        node = LeafNode("Just some plain text.") # Tag defaults to None
        self.assertEqual(node.to_html(), "Just some plain text.")
        node_explicit_none = LeafNode("More plain text.", None)
        self.assertEqual(node_explicit_none.to_html(), "More plain text.")


    # Test case 4: Tag with no props
    def test_to_html_no_props(self):
        """Tests rendering a tag (like <b>) that typically has no props."""
        # CORRECTED ORDER: value first, then tag
        node = LeafNode("Bold text", "b")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    # Test case 5: Ensure ValueError is raised if value is None
    def test_to_html_no_value(self):
        """Tests that ValueError is raised if value is None when calling to_html."""
        # Create with a dummy value first to satisfy constructor if it checked
        node = LeafNode("temporary value", "span")
        node.value = None # Manually set value to None to trigger the error in to_html
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: LeafNode requires a value.")

    # Test case 6: Check __repr__
    def test_repr(self):
        """Tests the __repr__ method for LeafNode."""
        # CORRECTED ORDER: value first, then tag, then props
        node = LeafNode("Link", "a", {"class": "btn"})
        expected_repr = "LeafNode(tag=a, value=Link, props={'class': 'btn'})"
        self.assertEqual(repr(node), expected_repr)

# Standard boilerplate to run tests
if __name__ == "__main__":
    unittest.main()