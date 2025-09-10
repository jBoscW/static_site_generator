import sys
from src.website_generator import delete_and_move, generate_pages_recursive

def main(basepath = '/'):    
    if len(sys.argv) > 1: 
        basepath = sys.argv[1]

    delete_and_move(public_dir='./public', static_dir='./static')

    generate_pages_recursive(
        dir_path_content = './content', 
        dest_dir_path = './public', 
        base_path = basepath,
        template_path = './template.html'
    )


if __name__ == "__main__":

    main()