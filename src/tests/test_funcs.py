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
    
    def multiple_bold_delimiters(self):
        nodes = [TextNode("This is *bold* and *also bold* text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
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
    
    #extract_markdown
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://www.boot.dev) and another [link2](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.boot.dev"), ("link2", "https://www.google.com")], matches)

    def test_extract_no_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with no links"
        )
        self.assertListEqual([], matches)
    
    def test_extract_with_nested_parentheses(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://en.wikipedia.org/wiki/Function_(mathematics))"
        )
        self.assertListEqual([("link", "https://en.wikipedia.org/wiki/Function_(mathematics)")], matches)
    
    #split_nodes_image_and_links
    def test_split_nodes_image_no_image(self):
        nodes = [TextNode("This is text with no images", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)
    
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )
    
    def test_multiple_nodes_some_with_images(self):
        nodes = [
            TextNode("This is text with no images", TextType.TEXT),
            TextNode("Here is an image ![alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("Another image ![second image](https://i.imgur.com/second.png) here", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is text with no images", TextType.TEXT),
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("Another image ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/second.png"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_nodes_test_link_functions(self):
        nodes = [
            TextNode("This is text with no links", TextType.TEXT),
            TextNode("Here is a link [boot.dev](https://www.boot.dev)", TextType.TEXT),
            TextNode("Another link [Google](https://www.google.com) here", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is text with no links", TextType.TEXT),
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("Another link ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_nodes_test_link_and_image_functions(self):
        nodes = [
            TextNode("This is text with no links or images", TextType.TEXT),
            TextNode("Here is a link [boot.dev](https://www.boot.dev) and an image ![alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("Another link [Google](https://www.google.com) and image ![second image](https://i.imgur.com/second.png) here", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        result = split_nodes_link(result)
        expected = [
            TextNode("This is text with no links or images", TextType.TEXT),
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("Another link ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and image ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/second.png"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    
    #text_to_textnodes
    def test_text_to_textnodes_no_formatting(self):
        text = "This is plain text."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is plain text.", TextType.TEXT)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_bold_and_italic(self):
        text = "This is **bold** and _italic_ text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_code_and_images_and_links(self):
        text = "Here is `code`, an image ![alt](https://i.imgur.com/zjjcJKZ.png), and a link [boot.dev](https://www.boot.dev)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(", and a link ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(nodes, expected)
    
        

if __name__ == "__main__":
    unittest.main()