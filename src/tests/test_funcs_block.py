import unittest

# from src.textnode import *
# from src.htmlnode import *
from src.funcs_block import *


class TestTextNode(unittest.TestCase): 
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

if __name__ == "__main__":
    unittest.main()
    