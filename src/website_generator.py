import os
import shutil
import src.blocks as blocks
from pathlib import Path

def delete_and_move(public_dir, static_dir):
    if not os.path.exists(static_dir):
        raise ValueError("static directory does not exist")

    static_tree = os.listdir(static_dir)
    for entry in static_tree: 
        entry_path = os.path.join(static_dir, entry)
        public_new_path = os.path.join(public_dir, entry)
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, public_dir)
        elif os.path.isdir(entry_path):
            os.mkdir(public_new_path)
            delete_and_move(public_new_path, entry_path)

def extract_title(markdown): 
    markdown = markdown.strip().split('\n')
    for line in markdown:
        line = line.strip()
        if line.startswith('# '):
            return line.lstrip('#').strip()
        
    raise Exception("Title must start with '# '")

def generate_page(from_path, dest_path, base_path, template_path): 
    print(f"Generating page from {from_path} to {dest_path} using template.")

    with open(from_path, 'r') as f: 
        original_md = f.read()
    with open(template_path, 'r') as f: 
        template = f.read()
    
    html_txt = blocks.markdown_to_html_node(original_md).to_html()
    title = extract_title(original_md)

    new_txt = template.replace("{{ Title }}", title)
    new_txt = new_txt.replace("{{ Content }}", html_txt)
    new_txt = new_txt.replace('href="/', 'href="' + base_path)
    new_txt = new_txt.replace('src="/', 'src="' + base_path)

    with open(dest_path, 'w') as f:
        f.write(new_txt)
    
def generate_pages_recursive(dir_path_content, dest_dir_path, base_path, template_path = './template.html'):
    content_tree = os.listdir(dir_path_content)
    for entry in content_tree:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry_path):
            p = Path(dest_path)
            #Path-library concatenation
            html_dest_path = p.parent / (p.stem + ".html") 
            generate_page(entry_path, html_dest_path, base_path, template_path)
        elif os.path.isdir(entry_path):
            if not os.path.isdir(dest_path): 
                os.mkdir(dest_path)
            generate_pages_recursive(entry_path, dest_path, base_path, template_path)