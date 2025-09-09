from src.textnode import TextNode, TextType
from src.htmlnode import ParentNode, LeafNode
import src.funcs as fu

from enum import Enum
import re

class BlockType(Enum): 
    PARAGRAPH = "p"
    HEADING = "heading--"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)
    types = [block_to_block_type(bloc) for bloc in blocks]

    html_nodes = block_and_type_to_html(blocks, types)
    return ParentNode('div', html_nodes)

#########

### level 2
def markdown_to_blocks(markdown_text): 
    blocks = markdown_text.split('\n\n')
    
    blocks = [bloc.strip() for bloc in blocks]

    return [bloc for bloc in blocks if bloc]


def block_to_block_type(markdown):
    lines = markdown.split('\n')
    markdown = markdown.strip()

    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if markdown.startswith("```") and lines[-1].startswith("```"): 
        return BlockType.CODE
    if markdown.startswith('> '): 
        if all(line.startswith('>') for line in lines):
            return BlockType.QUOTE
    if markdown.startswith('- '): 
        if all(line.startswith('- ') for line in lines):
            return BlockType.UNORDERED_LIST
    if markdown[0].isdigit():
        if all(re.match(r"\d+\. ", line) for line in lines):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_and_type_to_html(blocks, types):
    block_types = list(zip(blocks, types))
    html_nodes = []

    for txt, type in block_types:
        html_node = None
        match type:
            case BlockType.CODE: 
                html_node = create_code_html_node(txt)
            case BlockType.ORDERED_LIST:
                html_node = create_ordered_list_html_node(txt)
            case BlockType.UNORDERED_LIST:
                html_node = create_unordered_list_html_node(txt)
            case BlockType.HEADING: 
                html_node = create_heading_html_node(txt)
            case BlockType.PARAGRAPH: 
                html_node = create_other_html_node(txt, BlockType.PARAGRAPH)
            case BlockType.QUOTE: 
                html_node = create_other_html_node(txt, BlockType.QUOTE)
            case _: 
                raise ValueError('invalid BlockType')
            
        html_nodes.append(html_node)

    return html_nodes

###level 3 funcs
def create_code_html_node(txt):
    txt = txt[3:-3].strip()
    
    code_text_node = TextNode(txt, TextType.CODE)
    code_html_child = fu.text_node_to_html_node(code_text_node)
    
    return ParentNode('pre', [code_html_child])

def create_unordered_list_html_node(txt):
    lines = txt.split('\n')
    children = []
    for line in lines: 
        START_STRING = '- '
        line = line[len(START_STRING) :]
        txt_nodes = fu.text_to_textnodes(line)
        html_nodes = [fu.text_node_to_html_node(i) for i in txt_nodes]

        children.append(ParentNode('li', html_nodes))
    
    return ParentNode('ul', children)

        
def create_ordered_list_html_node(txt): 
    lines = txt.split('\n')
    children = []
    for line in lines: 
        START_STRING = r"\d+\. "
        match = re.match(START_STRING, line)
        line = line[match.end() :]
        txt_nodes = fu.text_to_textnodes(line)
        html_nodes = [fu.text_node_to_html_node(i) for i in txt_nodes]

        children.append(ParentNode('li', html_nodes))
    
    return ParentNode('ol', children)

def create_other_html_node(txt, blocktype):
    if blocktype is BlockType.QUOTE: 
        #skips '> '
        txt = '\n'.join(line[2:] for line in txt.split('\n')) 
    elif blocktype is BlockType.PARAGRAPH: 
        txt = txt.replace('\n', ' ')

    tag = blocktype.value
    txt_nodes = fu.text_to_textnodes(txt)
    html_nodes = [fu.text_node_to_html_node(i) for i in txt_nodes]

    return ParentNode(tag, html_nodes)

def create_heading_html_node(txt):
    heading_level = 0
    for char in txt: 
        if char == '#': 
            heading_level += 1
        else: 
            break

    tag = f'h{heading_level}'
    txt = txt[heading_level:].strip() # "## wow" becomes <h2>wow</h2>
    txt_nodes = fu.text_to_textnodes(txt)
    html_nodes = [fu.text_node_to_html_node(i) for i in txt_nodes]

    return ParentNode(tag, html_nodes)