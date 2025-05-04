import unittest

# Import necessary classes and the function to test
from textnode import TextNode, TextType
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):

    # Test case 1: Basic code block splitting (provided example)
    def test_split_code(self):
        """Tests basic splitting with the code delimiter."""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 2: Basic bold splitting
    def test_split_bold(self):
        """Tests basic splitting with the bold delimiter."""
        node = TextNode("Here is **bold text** for you", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" for you", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 3: Basic italic splitting
    def test_split_italic(self):
        """Tests basic splitting with the italic delimiter."""
        node = TextNode("An _italic phrase_ appears", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" appears", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 4: Delimiter at the beginning
    def test_split_delimiter_start(self):
        """Tests splitting when the delimited text is at the start."""
        node = TextNode("**Bold** starts the sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" starts the sentence", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 5: Delimiter at the end
    def test_split_delimiter_end(self):
        """Tests splitting when the delimited text is at the end."""
        node = TextNode("Sentence ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Sentence ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 6: Multiple delimited sections
    def test_split_multiple_delimiters(self):
        """Tests splitting with multiple delimited sections in one node."""
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 7: Only delimited text
    def test_split_only_delimited(self):
        """Tests splitting when the entire node text is delimited."""
        node = TextNode("**All Bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("All Bold", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 8: Non-TEXT node should pass through unchanged
    def test_split_non_text_node(self):
        """Tests that non-TEXT nodes are not affected."""
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More normal text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        # Only the "Normal text" and "More normal text" should be checked for splitting
        # Since they don't contain "**", they remain unchanged.
        expected = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More normal text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 9: Mixed nodes where one needs splitting
    def test_split_mixed_nodes_with_split(self):
        """Tests a list containing mixed node types where one needs splitting."""
        nodes = [
            TextNode("Prefix ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC), # Should pass through
            TextNode(" middle `code` suffix", TextType.TEXT), # Should be split
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Prefix ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" middle ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" suffix", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 10: No delimiter present in text node
    def test_split_no_delimiter(self):
        """Tests a TEXT node that doesn't contain the delimiter."""
        node = TextNode("This text has no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This text has no delimiter", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    # Test case 11: Error on unmatched delimiter
    def test_split_unmatched_delimiter(self):
        """Tests that ValueError is raised for unmatched delimiters."""
        node = TextNode("This `code block is not closed", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        # Optional: Check specific error message content
        self.assertIn("Unmatched delimiter '`'", str(cm.exception))

    # Test case 12: Adjacent delimiters (should produce empty text node if logic didn't skip)
    # Our logic skips empty strings, so this should be handled correctly.
    def test_split_adjacent_delimiters(self):
         """Tests handling of adjacent delimiters."""
         node = TextNode("Text with **** bold markers", TextType.TEXT)
         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
         expected = [
             TextNode("Text with ", TextType.TEXT),
             # The part between the first "**" and second "**" is empty, skipped by `if not part:`
             TextNode(" bold markers", TextType.TEXT),
         ]
         self.assertListEqual(new_nodes, expected)

    def test_extract_images_single(self):
        """Tests extracting a single image."""
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images_multiple(self):
        """Tests extracting multiple images."""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_no_images(self):
        """Tests text with no images."""
        text = "This text has no images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_images_mixed_with_links(self):
        """Tests extracting images when links are also present."""
        text = "Text with ![image](img.png) and a [link](link.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "img.png")], matches)

    def test_extract_images_empty_alt_url(self):
         """Tests images with empty alt or url."""
         text = "![empty alt]() and ![](/url.jpg)"
         matches = extract_markdown_images(text)
         expected = [
             ("empty alt", ""),
             ("", "/url.jpg")
         ]
         self.assertListEqual(expected, matches)


    # --- Tests for extract_markdown_links ---

    def test_extract_links_single(self):
        """Tests extracting a single link."""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_links_multiple(self):
        """Tests extracting multiple links."""
        text = "Link 1 [here](url1.com) and link 2 [there](url2.net)"
        matches = extract_markdown_links(text)
        expected = [
            ("here", "url1.com"),
            ("there", "url2.net")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_links_no_links(self):
        """Tests text with no links."""
        text = "This text has no actual links, only text."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_mixed_with_images(self):
        """Tests extracting links when images are also present."""
        text = "Text with ![image](img.png) and a [link](link.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "link.com")], matches)

    def test_extract_links_empty_anchor_url(self):
         """Tests links with empty anchor or url."""
         text = "[empty anchor]() and [](/url.org)"
         matches = extract_markdown_links(text)
         expected = [
             ("empty anchor", ""),
             ("", "/url.org")
         ]
         self.assertListEqual(expected, matches)
         
         
    def test_split_image_single(self):
        """Tests splitting a single image from a TEXT node."""
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png) in the middle.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" in the middle.", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_multiple(self):
        """Tests splitting multiple images (provided example)."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_start(self):
        """Tests splitting when image is at the start."""
        node = TextNode("![start image](start.jpg) rest of text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "start.jpg"),
            TextNode(" rest of text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_end(self):
        """Tests splitting when image is at the end."""
        node = TextNode("Text ends with ![end image](end.gif)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ends with ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "end.gif"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_only(self):
         """Tests splitting when the text is only an image."""
         node = TextNode("![just image](only.png)", TextType.TEXT)
         new_nodes = split_nodes_image([node])
         expected = [
             TextNode("just image", TextType.IMAGE, "only.png"),
         ]
         self.assertListEqual(expected, new_nodes)

    def test_split_image_no_image(self):
        """Tests splitting text with no images."""
        node = TextNode("Plain text node, no images here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes) # Should return the original node in a list

    def test_split_image_mixed_nodes(self):
        """Tests splitting with non-TEXT nodes present."""
        nodes = [
            TextNode("Prefix text ", TextType.TEXT),
            TextNode("![image1](img1.png)", TextType.TEXT),
            TextNode(" bold text ", TextType.BOLD), # Non-TEXT node
            TextNode("Suffix text ![image2](img2.jpg) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Prefix text ", TextType.TEXT),
            # Splitting of the second node
            TextNode("image1", TextType.IMAGE, "img1.png"),
            # The BOLD node passes through
            TextNode(" bold text ", TextType.BOLD),
            # Splitting of the fourth node
            TextNode("Suffix text ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "img2.jpg"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    # --- Tests for split_nodes_link ---

    def test_split_link_single(self):
        """Tests splitting a single link from a TEXT node."""
        node = TextNode(
            "Check out [this link](https://example.com) for details.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("this link", TextType.LINK, "https://example.com"),
            TextNode(" for details.", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_multiple(self):
        """Tests splitting multiple links (provided example)."""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_start(self):
        """Tests splitting when link is at the start."""
        node = TextNode("[start link](start.html) rest of text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "start.html"),
            TextNode(" rest of text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_end(self):
        """Tests splitting when link is at the end."""
        node = TextNode("Text ends with [end link](end.org)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ends with ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "end.org"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_only(self):
         """Tests splitting when the text is only a link."""
         node = TextNode("[just link](only.net)", TextType.TEXT)
         new_nodes = split_nodes_link([node])
         expected = [
             TextNode("just link", TextType.LINK, "only.net"),
         ]
         self.assertListEqual(expected, new_nodes)

    def test_split_link_no_link(self):
        """Tests splitting text with no links."""
        node = TextNode("Plain text node, no links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes) # Should return the original node in a list

    def test_split_link_ignores_image(self):
        """Tests that split_nodes_link ignores image markdown."""
        node = TextNode(
            "Text with ![image](img.png) and [link](link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            # Image is treated as plain text here
            TextNode("Text with ![image](img.png) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
        ]
        self.assertListEqual(expected, new_nodes)         
         
    def test_text_to_textnodes_example(self):
        """Tests the main example provided in the assignment."""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        """Tests conversion of plain text with no markdown."""
        text = "Just some plain text without any special formatting."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Just some plain text without any special formatting.", TextType.TEXT)
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_bold(self):
        """Tests conversion with only bold elements."""
        text = "**This** whole sentence is **bold**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" whole sentence is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_adjacent_elements(self):
        """Tests conversion with adjacent markdown elements."""
        text = "An image ![img](url.png) followed by a [link](url.com) and `code`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("An image ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.png"),
            TextNode(" followed by a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_starts_and_ends(self):
        """Tests conversion when markdown is at the start and end."""
        text = "`Start code` middle text ![End Image](end.gif)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start code", TextType.CODE),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("End Image", TextType.IMAGE, "end.gif"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty_string(self):
         """Tests conversion of an empty string."""
         text = ""
         nodes = text_to_textnodes(text)
         # Should result in a single TextNode with empty text, which the splitters should handle
         # Or potentially an empty list if the initial node is filtered/not added.
         # Let's assume the current logic keeps the empty node.
         # Refined: If the initial text is empty, the list starts with TextNode("", "text").
         # split_nodes_image/link on this node return [TextNode("", "text")].
         # split_nodes_delimiter on this node return [TextNode("", "text")].
         # So it *should* return a list containing one empty text node.
         # Update: Let's refine the expectation to an empty list, assuming empty nodes aren't useful.
         # The split functions *should* prevent adding empty nodes. Let's test that.
         # Rerun thought: The current splitters *do* have `if text_before:` checks.
         # An empty input `text=""` -> `initial_node = TextNode("", "text")`.
         # `split_nodes_image([TextNode("", "text")])` -> extracts nothing -> returns `[]` because `original_text` is empty.
         # So, the expected output for an empty string should be an empty list.
         expected = []
         self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_delimiters(self):
        """Tests conversion with multiple instances of the same delimiter type."""
        text = "Some _italic_ text and more _italic_ here."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and more ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)         
         
# Standard boilerplate
if __name__ == "__main__":
    unittest.main()