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

    shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)
    delete_and_move(dir_path_public, dir_path_static)

    generate_pages_recursive(
        dir_path_content = (dir_path_content),
        dest_dir_path = (dir_path_public),
        template_path = (template_path),
        base_path = basepath
    )


if __name__ == "__main__":
    main()