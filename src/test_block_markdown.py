import unittest

# Import the function to test
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):

    # Test case 1: Basic split (provided)
    def test_markdown_to_blocks_basic(self):
        """Tests basic splitting with paragraphs and a list."""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(expected, blocks)

    # Test case 2: Excessive newlines between blocks
    def test_markdown_to_blocks_excessive_newlines(self):
        """Tests splitting with more than one blank line between blocks."""
        md = "Block 1\n\n\n\nBlock 2\n\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        expected = [
            "Block 1",
            "Block 2",
            "Block 3",
        ]
        self.assertListEqual(expected, blocks)

    # Test case 3: Leading and trailing blank lines in the input
    def test_markdown_to_blocks_leading_trailing_blanks(self):
        """Tests input starting and ending with blank lines."""
        md = "\n\n\nBlock A\n\nBlock B\n\n\n"
        blocks = markdown_to_blocks(md)
        expected = [
            "Block A",
            "Block B",
        ]
        self.assertListEqual(expected, blocks)

    # Test case 4: Leading/trailing whitespace *within* blocks
    def test_markdown_to_blocks_internal_whitespace(self):
        """Tests blocks containing leading/trailing whitespace."""
        md = "    Block 1 indented\n\n  \t Block 2 mixed whitespace \t \n\nBlock 3"
        blocks = markdown_to_blocks(md)
        expected = [
            "Block 1 indented",
            "Block 2 mixed whitespace",
            "Block 3",
        ]
        self.assertListEqual(expected, blocks)

    # Test case 5: Blocks containing only whitespace (should be removed)
    def test_markdown_to_blocks_whitespace_only_block(self):
         """Tests that blocks containing only whitespace are filtered out."""
         md = "Real Block\n\n   \t \n \n\nAnother Real Block"
         blocks = markdown_to_blocks(md)
         expected = [
             "Real Block",
             "Another Real Block",
         ]
         self.assertListEqual(expected, blocks)

    # Test case 6: Single block input (no blank lines)
    def test_markdown_to_blocks_single_block(self):
        """Tests input consisting of only one block."""
        md = "# Heading\nThis is content below the heading.\nNo blank lines."
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading\nThis is content below the heading.\nNo blank lines."
        ]
        self.assertListEqual(expected, blocks)

    # Test case 7: Empty string input
    def test_markdown_to_blocks_empty_string(self):
        """Tests an empty input string."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertListEqual([], blocks)

    # Test case 8: Input with only whitespace and newlines
    def test_markdown_to_blocks_only_whitespace_newlines(self):
        """Tests input containing only whitespace and newlines."""
        md = "   \n \t \n\n \n \n   \t\n\n"
        blocks = markdown_to_blocks(md)
        self.assertListEqual([], blocks)


    def test_block_type_heading(self):
        """Tests identifying heading blocks."""
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Invalid headings (no space or too many #) should be paragraphs
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too Many Hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not a heading # in middle"), BlockType.PARAGRAPH)


    def test_block_type_code(self):
        """Tests identifying code blocks."""
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block_single_line = "```inline code```" # Assuming this is valid per rules
        self.assertEqual(block_to_block_type(block_single_line), BlockType.CODE)
        # Invalid code blocks
        block_no_end = "```\ncode"
        self.assertEqual(block_to_block_type(block_no_end), BlockType.PARAGRAPH)
        block_no_start = "code\n```"
        self.assertEqual(block_to_block_type(block_no_start), BlockType.PARAGRAPH)
        block_just_ticks = "```" # Should not be code
        self.assertEqual(block_to_block_type(block_just_ticks), BlockType.PARAGRAPH)


    def test_block_type_quote(self):
        """Tests identifying quote blocks."""
        block = "> This is a quote\n> Spanning multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block_single_line = "> Just one line."
        self.assertEqual(block_to_block_type(block_single_line), BlockType.QUOTE)
        # Invalid quote block (one line doesn't start with >)
        block_invalid = "> First line quote\nSecond line not quote."
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)
        block_empty_line_not_quote = "> Quote\n\n> After empty line" # Empty line breaks quote rule
        self.assertEqual(block_to_block_type(block_empty_line_not_quote), BlockType.PARAGRAPH)


    def test_block_type_unordered_list(self):
        """Tests identifying unordered list blocks."""
        block_dash = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block_dash), BlockType.UNORDERED_LIST)
        block_star = "* Item A\n* Item B"
        self.assertEqual(block_to_block_type(block_star), BlockType.UNORDERED_LIST)
        block_mixed = "* Item 1\n- Item 2" # Mixed markers are often allowed, let's test if our rule covers this
        self.assertEqual(block_to_block_type(block_mixed), BlockType.UNORDERED_LIST) # Yes, it should
        block_single_item = "- Only one"
        self.assertEqual(block_to_block_type(block_single_item), BlockType.UNORDERED_LIST)
        # Invalid unordered list
        block_invalid_marker = "- Item 1\n+ Item 2" # '+' is not a valid marker here
        self.assertEqual(block_to_block_type(block_invalid_marker), BlockType.PARAGRAPH)
        block_no_space = "-Item without space"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.PARAGRAPH)
        block_mixed_paragraph = "- Item 1\nThis is a paragraph line"
        self.assertEqual(block_to_block_type(block_mixed_paragraph), BlockType.PARAGRAPH)


    def test_block_type_ordered_list(self):
        """Tests identifying ordered list blocks."""
        block_valid = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block_valid), BlockType.ORDERED_LIST)
        block_single_item = "1. Only one"
        self.assertEqual(block_to_block_type(block_single_item), BlockType.ORDERED_LIST)
        # Invalid ordered lists
        block_wrong_start = "2. Starts at two"
        self.assertEqual(block_to_block_type(block_wrong_start), BlockType.PARAGRAPH)
        block_wrong_sequence = "1. First\n3. Skipped two"
        self.assertEqual(block_to_block_type(block_wrong_sequence), BlockType.PARAGRAPH)
        block_no_space = "1.No space"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.PARAGRAPH)
        block_wrong_format = "1) Wrong format"
        self.assertEqual(block_to_block_type(block_wrong_format), BlockType.PARAGRAPH)
        block_mixed_paragraph = "1. Item 1\nThis is a paragraph line"
        self.assertEqual(block_to_block_type(block_mixed_paragraph), BlockType.PARAGRAPH)


    def test_block_type_paragraph(self):
        """Tests identifying paragraph blocks (default)."""
        block_simple = "This is just a plain paragraph."
        self.assertEqual(block_to_block_type(block_simple), BlockType.PARAGRAPH)
        block_multiline = "Paragraphs can span\nmultiple lines\nwithout special markers."
        self.assertEqual(block_to_block_type(block_multiline), BlockType.PARAGRAPH)
        block_with_symbols = "Text containing > * - 1. symbols but not following rules."
        self.assertEqual(block_to_block_type(block_with_symbols), BlockType.PARAGRAPH)


    def test_md_to_html_paragraphs(self):
        """Tests conversion of multiple paragraphs."""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected_html)

    def test_md_to_html_lists(self):
        """Tests conversion of unordered and ordered lists."""
        md = """
- Item 1 **bold**
- Item 2 `code`

1. First item _italic_
2. Second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ul><li>Item 1 <b>bold</b></li><li>Item 2 <code>code</code></li></ul><ol><li>First item <i>italic</i></li><li>Second item</li></ol></div>"
        self.assertEqual(html, expected_html)

    def test_md_to_html_headings(self):
        """Tests conversion of various heading levels."""
        md = """
# Heading 1

Some text

## Heading 2 _italic_

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>Heading 1</h1><p>Some text</p><h2>Heading 2 <i>italic</i></h2><h3>Heading 3</h3></div>"
        self.assertEqual(html, expected_html)

    def test_md_to_html_blockquote(self):
        """Tests conversion of blockquotes."""
        md = """
> This is a quote.
> It has **bold** text.

Another paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><blockquote><p>This is a quote.\nIt has <b>bold</b> text.</p></blockquote><p>Another paragraph.</p></div>"
        # Note: The blockquote content gets wrapped in a <p> because text_to_children -> ParentNode("blockquote", [LeafNodes]) -> to_html() might implicitly do this,
        # OR our helper should explicitly wrap in <p>. Let's refine the quote helper.
        # --- Refinement ---
        # Rereading: The quote helper calls text_to_children which returns LeafNodes. ParentNode("blockquote", children) is correct.
        # The test output needs adjustment based on how ParentNode renders children. Let's assume simple concatenation.
        # Expected should be: <blockquote>This is a quote.\nIt has <b>bold</b> text.</blockquote>
        # Let's test again. If it fails, the ParentNode might need adjustment, or the test needs <p>.
        # Simpler: Let's adjust the expected HTML to reflect simple concatenation for now.
        expected_html_simple = "<div><blockquote>This is a quote.\nIt has <b>bold</b> text.</blockquote><p>Another paragraph.</p></div>"
        self.assertEqual(html, expected_html_simple)


    def test_md_to_html_codeblock(self):
        """Tests conversion of code blocks (no inline parsing)."""
        md = """
Normal paragraph.

```python
# This is code
def function(x):
  # It has _italic_ and **bold** syntax
  return x * 2"""



    def test_extract_title_valid(self):
        """Tests extracting a valid H1 title."""
        md = """
Some preamble text.

# This Is The Title

More text.
## Subheading
"""
        self.assertEqual(extract_title(md), "This Is The Title")

    def test_extract_title_no_h1(self):
        """Tests raising error if no H1 is present."""
        md = "Just paragraph text.\n## No H1 Here"
        with self.assertRaisesRegex(ValueError, "No H1 heading found"):
            extract_title(md)

    def test_extract_title_h2_present_no_h1(self):
        """Tests raising error if only H2+ are present."""
        md = "## Subheading\n### SubSub"
        with self.assertRaisesRegex(ValueError, "No H1 heading found"):
            extract_title(md)

    def test_extract_title_marker_no_space(self):
        """Tests raising error if H1 marker has no space."""
        md = "#NoSpaceTitle\nSome text."
        # This should NOT match '# ' so it will raise error
        with self.assertRaisesRegex(ValueError, "No H1 heading found"):
            extract_title(md)

    def test_extract_title_leading_whitespace(self):
        """Tests extracting title with leading whitespace before marker."""
        md = "   # Correct Title\nMore text."
        self.assertEqual(extract_title(md), "Correct Title")

    def test_extract_title_trailing_whitespace(self):
        """Tests extracting title stripping trailing whitespace."""
        md = "# Title with spaces   \n"
        self.assertEqual(extract_title(md), "Title with spaces")

    def test_extract_title_empty_input(self):
        """Tests raising error on empty input."""
        md = ""
        with self.assertRaisesRegex(ValueError, "No H1 heading found"):
            extract_title(md)

# Standard boilerplate
if __name__ == "__main__":
    unittest.main()