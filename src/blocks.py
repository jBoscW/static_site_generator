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
    
    return list(zip(blocks, types))

#########

### level 2
def markdown_to_blocks(markdown_text): 
    blocks = markdown_text.split('\n\n')
    
    blocks = [bloc.strip() for bloc in blocks]

    return [bloc for bloc in blocks if bloc]


def block_to_block_type(markdown):
    first_word = markdown.split()[0]
    if len(set(first_word)) == 1 and len(first_word) <= 6 and '#' in first_word:
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"): 
        return BlockType.CODE
    
    quote, unord, orde = True, True, True
    for line in markdown.split('\n'): 
        if not line.startswith('>'):
            quote = False
        if not line.startswith('- '): 
            unord = False
        if not quote and not unord: 
            break

    if quote: return BlockType.QUOTE
    if unord: return BlockType.UNORDERED_LIST

    num = 1
    for line in markdown.split('\n'): 
        if not line.startswith(f"{num}. "):
            orde = False
            break
        num += 1
    if orde: return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def block_and_type_to_html(blocks, types):
    block_types = list(zip(blocks, types))
    children_body = []

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
                html_node = create_other_html_node
            case BlockType.PARAGRAPH: 
                html_node = create_other_html_node(txt, BlockType.PARAGRAPH)
            case BlockType.QUOTE: 
                html_node = create_other_html_node(txt, BlockType.QUOTE)
            
        children_body.append(html_node)
            

    main_node = ParentNode(tag='div', children=children_body)
    return main_node

###level 3 funcs
def create_code_html_node(txt):
    txt = txt[3:-3].strip() # bc of ```code ``` md styling

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

        li_node = ParentNode('li', html_nodes)
        children.append(li_node)
    
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

        li_node = ParentNode('li', html_nodes)
        children.append(li_node)
    
    return ParentNode('ol', children)

def create_other_html_node(txt, blocktype):
    if blocktype is BlockType.QUOTE: 
        txt = txt[2:] #skips '> '

    tag = blocktype.value
    txt_nodes = fu.text_to_textnodes(txt)
    html_nodes = [fu.text_node_to_html_node(i) for i in txt_nodes]

    return ParentNode(tag, html_nodes)

def create_heading_html_node(txt):
    heading_level = len(txt.split()[0])
    tag = f'h{heading_level}'

    txt = txt[heading_level + 1: ] # "## wow" becomes <h2>wow</h2>
    txt_nodes = fu.text_to_textnodes(txt)
    html_nodes = [fu.text_node_to_html_node(i) for i in txt_nodes]

    return ParentNode(tag, html_nodes)
    

####level 3.5 func
# def block_type_to_parent_node(type, children, heading_level=None): 
#     match type: 
#         case BlockType.PARAGRAPH: 
#             return ParentNode('p', children)
#         case BlockType.HEADING:
#             if heading_level is None: 
#                 raise ValueError("heading level must be provided for heading block type")
#             heading_tag = f'h{heading_level}'
#             return ParentNode(heading_tag, children)
#         case BlockType.CODE: 
#             return ParentNode('pre', children)
#         case BlockType.QUOTE:
#             return ParentNode('blockquote', children)
#         case BlockType.UNORDERED_LIST:
#             ## add a function in the main func so the children are all parent nodes with <li>
#             return ParentNode('ul', children)
#         case BlockType.ORDERED_LIST: 
#             ## add a function in the main func so the children are all parent nodes with <li>
#             return ParentNode('ol', children)
#         case _: 
#             raise ValueError('Not. ablock type -bich')
