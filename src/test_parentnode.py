import unittest

from htmlnode import ParentNode, LeafNode # Import necessary classes

class TestParentNode(unittest.TestCase):

    # Test case 1: Basic children (provided)
    def test_to_html_with_children(self):
        """Tests rendering a parent with simple leaf children."""
        # CORRECTED LeafNode call: value first, then tag
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # Test case 2: Nested parents (grandchildren) (provided)
    def test_to_html_with_grandchildren(self):
        """Tests rendering nested parent nodes."""
        # CORRECTED LeafNode call: value first, then tag
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Test case 3: Multiple direct children
    def test_to_html_multiple_children(self):
        """Tests rendering with multiple sibling leaf nodes."""
        node = ParentNode(
            "p",
            [
                # CORRECTED LeafNode calls: value first, then tag (or None)
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None), # Raw text node
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    # Test case 4: Parent node with properties
    def test_to_html_with_props(self):
        """Tests rendering a parent node that has HTML attributes."""
        # CORRECTED LeafNode call: value first, then tag (None)
        node = ParentNode(
            "a",
            [LeafNode("Click here", None)], # Raw text inside link
            {"href": "https://boot.dev", "target": "_blank"}
        )
        expected_html_start = '<a href="https://boot.dev" target="_blank">'
        expected_html_end = 'Click here</a>'
        # Account for potential attribute order differences
        result = node.to_html()
        self.assertTrue(result.startswith("<a "))
        self.assertIn('href="https://boot.dev"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.endswith(expected_html_end))


    # Test case 5: Deeper nesting (3 levels)
    def test_to_html_deep_nesting(self):
        """Tests rendering with three levels of nesting."""
        # CORRECTED LeafNode calls: value first, then tag (or None)
        gg_child = LeafNode("Deep", "i")
        g_child = ParentNode("span", [gg_child])
        child = ParentNode("p", [LeafNode("Text ", None), g_child]) # Mix leaf and parent
        parent = ParentNode("div", [child])
        expected_html = "<div><p>Text <span><i>Deep</i></span></p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    # Test case 6: No children (empty list)
    def test_to_html_no_children_empty_list(self):
        """Tests rendering when the children list is empty."""
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    # Test case 7: Error - No tag
    def test_error_no_tag(self):
        """Tests ValueError is raised if tag is missing."""
        # CORRECTED LeafNode call
        node = ParentNode(None, [LeafNode("child", "span")]) # Tag is None
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertIn("requires a tag", str(cm.exception))

        # CORRECTED LeafNode call
        node_empty_tag = ParentNode("", [LeafNode("child", "span")])
        with self.assertRaises(ValueError) as cm:
             node_empty_tag.to_html()
        self.assertIn("requires a tag", str(cm.exception))


    # Test case 8: Error - Children is None
    def test_error_children_is_none(self):
        """Tests ValueError is raised if children is None."""
        node = ParentNode("p", None) # Children is None
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertIn("requires children", str(cm.exception))

# Standard boilerplate to run tests
if __name__ == "__main__":
    unittest.main()