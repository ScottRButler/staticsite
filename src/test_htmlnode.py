import unittest

# Import the class we want to test
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    # Test case 1: Basic props conversion
    def test_props_to_html_basic(self):
        """Tests conversion of a basic props dictionary."""
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_html)

    # Test case 2: Props with different ordering (should still work)
    def test_props_to_html_ordering(self):
        """Tests if order matters (it shouldn't for the final string structure)."""
        # Note: Dictionary order is guaranteed in Python 3.7+, but the logic
        #       should produce the same *set* of attributes regardless.
        #       The exact string order might vary based on dict insertion order
        #       before 3.7, but the components should be correct.
        node = HTMLNode(props={"target": "_blank", "href": "https://test.com"})
        # We check if both expected parts are present, accounting for potential order variation
        result = node.props_to_html()
        self.assertIn(' href="https://test.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertTrue(result.startswith(" ")) # Check leading space
        self.assertEqual(len(result.split(' ')), 3) # Space + 2 attrs = 3 parts

    # Test case 3: No props (props=None)
    def test_props_to_html_none(self):
        """Tests props_to_html when props is None."""
        node = HTMLNode(tag="p", value="Hello") # props defaults to None
        self.assertEqual(node.props_to_html(), "")

    # Test case 4: Empty props dictionary (props={})
    def test_props_to_html_empty(self):
        """Tests props_to_html with an empty dictionary."""
        node = HTMLNode(tag="div", props={})
        self.assertEqual(node.props_to_html(), "")

    # Test case 5: Single prop
    def test_props_to_html_single(self):
        """Tests props_to_html with a single attribute."""
        node = HTMLNode(tag="img", props={"src": "image.png", "alt": "My Image"})
        expected1 = ' src="image.png" alt="My Image"'
        expected2 = ' alt="My Image" src="image.png"' # Account for potential order diff
        result = node.props_to_html()
        self.assertTrue(result == expected1 or result == expected2)


    # Test case 6: Check __repr__ for debugging usefulness (optional but good)
    def test_repr_output(self):
        """Tests the __repr__ method for a clear representation."""
        node = HTMLNode("a", "Click me", None, {"href": "https://boot.dev"})
        expected_repr = "HTMLNode(tag=a, value=Click me, children=None, props={'href': 'https://boot.dev'})"
        self.assertEqual(repr(node), expected_repr)

    # Test case 7: Test to_html raises NotImplementedError (as required)
    def test_to_html_raises_error(self):
        """Tests that the base to_html method raises NotImplementedError."""
        node = HTMLNode()
        # Use assertRaises to check if the specific error is raised when calling the method
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()