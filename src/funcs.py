from .textnode import TextNode, TextType
from .htmlnode import *
import re

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
    # to avoid delimiter == ""
    if not delimiter: 
        raise ValueError("delimiter must be non-empty")

    new_nodes = []
    for node in old_nodes: 
        if node.text_type is not TextType.TEXT: 
            new_nodes.append(node)
            continue

        s = node.text
        if delimiter not in s: 
            new_nodes.append(node)
            continue

        md_text = s.split(delimiter)
        if len(md_text) % 2 == 0: 
            raise ValueError(f"unmatched delimiter {delimiter!r} in: {s!r}")

        
        for i, text in enumerate(md_text):
            if text == '': 
                continue
            elif i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else: 
                new_nodes.append(TextNode(text, text_type))
            
    return new_nodes

#ex: ![image](https://i.imgur.com/zjjcJKZ.png)
def extract_markdown_images(text): 
     regex = r"!\[([^\[\]]*)\]\(((?:[^\s()]|\([^\s()]*\))*)\)"
     return re.findall(regex, text)

#ex: [link](https://www.boot.dev)
def extract_markdown_links(text): 
    regex = r"(?<!!)\[([^\[\]]*)\]\(((?:[^\s()]|\([^\s()]*\))*)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes):
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT: 
            out.append(node)
            continue
        
        s = node.text
        extracted_imgs = extract_markdown_images(s) #list of tuples
        if not extracted_imgs:
            out.append(node)
            continue
        
        start_index = 0
        while extracted_imgs: 
            img_text, url = extracted_imgs.pop(0)
            text_url = f'![{img_text}]({url})'
            regular_text = s[start_index:].split(text_url)

            if regular_text[0]:
                out.append(TextNode(regular_text[0], TextType.TEXT))

            out.append(TextNode(img_text, TextType.IMAGE, url))

            start_index = s.find(text_url, start_index)
            if start_index == -1:
                raise ValueError('brother, text_url link not found')
            start_index += len(text_url)
        
        if regular_text[1]:
            out.append(TextNode(regular_text[1], TextType.TEXT))

    return out
            


def split_nodes_link(old_nodes):
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT: 
            out.append(node)
            continue
        
        s = node.text
        extracted_links = extract_markdown_links(s) #list of tuples
        if not extracted_links:
            out.append(node)
            continue
        
        start_index = 0
        while extracted_links: 
            text, url = extracted_links.pop(0)
            text_url = f'[{text}]({url})'
            regular_text = s[start_index:].split(text_url, maxsplit=1)

            out.append(TextNode(regular_text[0], TextType.TEXT))
            out.append(TextNode(text, TextType.LINK, url))

            start_index = s.find(text_url, start_index) + len(text_url)
            if start_index == -1:
                raise ValueError('brother, text_url link not found')
        
        if regular_text[1]:
            out.append(TextNode(regular_text[1], TextType.TEXT))

    return out

def text_to_textnodes(text):
    text = [TextNode(text, TextType.TEXT)]
    text = split_nodes_delimiter(text, '**', TextType.BOLD)
    text = split_nodes_delimiter(text, '_', TextType.ITALIC)
    text = split_nodes_delimiter(text, '`', TextType.CODE)
    text = split_nodes_image(text)
    text = split_nodes_link(text)

    return text