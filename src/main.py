from .textnode import TextNode, TextType
from .htmlnode import *
from .funcs import *
from .blocks import *
from .website_generator import *

def main(): 
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    delete_and_move(public_dir='./public', static_dir='./static')
    print(extract_title(' # afkdj   '))


if __name__ == "__main__":
    main()