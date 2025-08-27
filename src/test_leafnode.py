import unittest

from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("li", "Hello, world!")
        self.assertEqual(node.to_html(), "<li>Hello, world!</li>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me!</a>')
    
    def test_leaf_to_html_and_super(self): 
        node1 = LeafNode("p", "Hello, world!", props={"class": "text"})
        node2 = LeafNode("p", "Hello, world!", props={"class": "text"})
        
        self.assertNotEqual(node1, node2)
        self.assertEqual(node1.props_to_html(), ' class="text"')
        self.assertEqual(node1.value, "Hello, world!")
        self.assertEqual(node2.children, None)
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
        