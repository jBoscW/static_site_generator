import unittest

# from src.textnode import *
# from src.htmlnode import *
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
    def test_block_types(self):
        md = """This is a paragraph.

### This is a heading

```python```
"""
        blocks = markdown_to_html_node(md)
        # i am testing if it creates a zipped list of block and BlockType tuples
        expected = [
            ("This is a paragraph.", BlockType.PARAGRAPH),
            ("### This is a heading", BlockType.HEADING),
            ("```python```", BlockType.CODE)
        ]
        self.assertListEqual(blocks, expected)

if __name__ == "__main__":
    unittest.main()
    