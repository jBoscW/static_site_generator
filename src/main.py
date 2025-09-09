from src.textnode import TextNode, TextType
from src.htmlnode import *
from src.funcs import *
from src.blocks import *
from src.website_generator import *

def main(): 
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    delete_and_move(public_dir='./public', static_dir='./static')

    generate_page(
        from_path='./content/index.md', 
        dest_path='./public/index.html',
    )



if __name__ == "__main__":
    main()