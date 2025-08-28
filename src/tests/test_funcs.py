import unittest

from src.textnode import *
from src.htmlnode import *
from src.funcs import *


class TestTextNode(unittest.TestCase):

    #text_node_to_html_node
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
    
    def test_img(self):
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.png",
            "alt": "An image"
        })
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.png" alt="An image"></img>')  # Remove this print

    def test_invalid_type(self):
        node = TextNode("Invalid", text_type="invalid_type")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Not a valid TextType")

    #split_nodes_delimiter
    def test_no_delimiter(self):
        nodes = [TextNode("No delimiter here", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(result, nodes)
    
    def test_single_pair_delimiter(self):
        nodes = [TextNode("This is *bold* text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_pairs_delimiter(self):
        nodes = [TextNode("This is *bold* and this is *also bold*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD)
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_old_nodes(self):
        nodes = [
            TextNode("First *bold* text", TextType.TEXT),
            TextNode("Second _italic_ text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()