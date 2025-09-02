from .textnode import TextNode, TextType
from .htmlnode import *

import funcs as f
from enum import Enum

class BlockType(Enum): 
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown): 

    blocks = markdown_to_blocks(markdown)
    block_types = block_and_type_tuple_generator(blocks)
    

####

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
    
    quote, unord, ord = True, True, True
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
            ord = False
            break
        num += 1
    if ord: return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def block_and_type_tuple_generator(blocks): 
    types = [block_to_block_type(bloc) for bloc in blocks]
    return zip(blocks, types)

