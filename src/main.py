import sys
from src.website_generator import * 

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1: 
        basepath = sys.argv[1]
        b = lambda path: str(basepath) + path[2:]
    else: 
        b = lambda x: x

    shutil.rmtree(b(dir_path_public))
    os.mkdir(b(dir_path_public))
    delete_and_move(b(dir_path_public), b(dir_path_static))

    generate_pages_recursive(
        dir_path_content = b(dir_path_content),
        dest_dir_path = b(dir_path_public),
        base_path = b(basepath),
        template_path = b(template_path)
    )


if __name__ == "__main__":
    main()