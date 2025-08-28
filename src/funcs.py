from .textnode import TextNode, TextType
from .htmlnode import *

def text_node_to_html_node(text_node): 
    match text_node.text_type: 
        case TextType.TEXT: 
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD: 
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC: 
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE: 
            return LeafNode(tag='code', value=text_node.text)
        case TextType.LINK: 
            return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
        case TextType.IMAGE: 
            return LeafNode(tag='img', value='', props={
                'src': text_node.url,
                'alt': text_node.text
                }
            )
        case _: 
            raise Exception('Not a valid TextType')

def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        md_text = node.text.split(delimiter)
        if len(md_text) % 2 == 0: 
            raise Exception('not an even number of delimiters')
        newly_separated = []
        for i in range(len(md_text)): 
            if i % 2 == 0:
                newly_separated.append(TextNode(md_text[i], TextType.TEXT))
            else: 
                newly_separated.append(TextNode(md_text[i], text_type))
        newly_separated = [x for x in newly_separated if x.text != '']
        new_nodes.extend(newly_separated)
    
    return new_nodes

