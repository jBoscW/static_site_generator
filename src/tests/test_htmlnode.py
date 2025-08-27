import unittest

from src.htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_NOT_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertNotEqual(node1, node2)

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="Hello")
        self.assertNotEqual(node.props_to_html(), "ooga booga")
    
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Link", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')
    
    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        self.assertEqual(repr(node), "HTMLNode(tag = p, value = Hello, children = None, props = {'class': 'text'})")


if __name__ == "__main__":
    unittest.main()