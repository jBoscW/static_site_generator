from .textnode import TextNode, TextType
from .htmlnode import *
from .funcs import *

def markdown_to_blocks(markdown_text): 
    blocks = markdown_text.split('\n\n')
    
    blocks = [bloc.strip() for bloc in blocks]

    return [bloc for bloc in blocks if bloc]

