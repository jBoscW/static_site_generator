import unittest
from src.blocks import *


class TestTextNode(unittest.TestCase): 
    # Test the markdown_to_blocks function
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        md = "\n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_trailing_newlines_and_trailing_whitespace(self):
        md = "  \n\nThis is a paragraph with trailing whitespace and newlines\n\n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with trailing whitespace and newlines"])
    
    # Test the block_to_block_type function
    def test_block_to_block_type_multiple_blocks_in_a_list(self):
        block_types = {
            "This is a paragraph": BlockType.PARAGRAPH,
            "### This is a heading": BlockType.HEADING,
            "###### This is a smaller heading": BlockType.HEADING,
            "```python\nprint('Hello, world!')\n```": BlockType.CODE,
            "> This is a quote\n> with multiple lines": BlockType.QUOTE,
            "- This is an unordered list\n- with multiple items": BlockType.UNORDERED_LIST,
            "1. This is an ordered list\n2. with multiple items": BlockType.ORDERED_LIST
        }

        for block, expected_type in block_types.items():
            self.assertEqual(block_to_block_type(block), expected_type) 
    
    def test_convert_md_to_block_then_check_types(self):
        md = """
    This is a paragraph.
    
    ### This is a heading
    
    ```python
    def hello():
        print('Hello, gay!')
    ```
    
    > This is a quote
    > with multiple lines
    
    - Item 1
    - Item 2
    
    1. First item
    2. Second item"""
        blocks = markdown_to_blocks(md)
        expected_types = [
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST
        ]
        
        for block, expected_type in zip(blocks, expected_types):
            self.assertEqual(
                block_to_block_type(block),
                expected_type,
                f"Expected {expected_type} for block: {block}"
            )
    
    #markdown_to_html_node
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_multiple_lists_and_quote(self):
        md = """
> This is a quote

- This is a list
- with items

1. First item
2. Second item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote><ul><li>This is a list</li><li>with items</li></ul><ol><li>First item</li><li>Second item</li></ol></div>",
        )

    def test_heading_levels_and_mixed_content(self):
        md = """
# Heading 1

wow words

```
Some `inline code` here
```

## Heading 2

Some more text with **bold** and _italic_ styles.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><p>wow words</p><pre><code>Some `inline code` here</code></pre><h2>Heading 2</h2><p>Some more text with <b>bold</b> and <i>italic</i> styles.</p></div>",
        )

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_invalid_code_block(self):
        md = """
```
This is an invalid code block because it does not end properly.
"""
        with self.assertRaises(ValueError) as context:
            node = markdown_to_html_node(md)
        self.assertIn("unmatched delimiter", str(context.exception))

if __name__ == "__main__":
    unittest.main()
    