import os
import shutil
import src.blocks as blocks

def delete_and_move(public_dir, static_dir, deleted=False):
    if not os.path.exists(static_dir):
        raise ValueError("static directory does not exist")
    
    if deleted == False:
        print(f"deleting {public_dir} and contents: {os.listdir(public_dir)}")
        print('creating new one')
        shutil.rmtree(public_dir)
        os.mkdir(public_dir)
        deleted = True

    static_tree = os.listdir(static_dir)
    for entry in static_tree: 
        entry_path = os.path.join(static_dir, entry)
        public_new_path = os.path.join(public_dir, entry)
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, public_dir)
        elif os.path.isdir(entry_path):
            os.mkdir(public_new_path)
            delete_and_move(public_new_path, entry_path, deleted=True)

def extract_title(markdown): 
    markdown = markdown.strip().split('\n')
    for line in markdown:
        line = line.strip()
        if line.startswith('# '):
            return line.lstrip('#').strip()
        
    raise Exception("Title must start with '# '")

def generate_page(from_path, dest_path, template_path = './template.html'): 
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, 'r') as f: 
        original_md = f.read()
    with open(template_path, 'r') as f: 
        template = f.read()
    
    html_txt = blocks.markdown_to_html_node(original_md).to_html()
    title = extract_title(original_md)
    new_txt = template.replace("{{ Title }}", title)
    new_txt = new_txt.replace("{{ Content }}", html_txt)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(new_txt)
    
def generate_pages_recursive(dir_path_content, dest_dir_path, template_path = './template.html'):
    template_abspath = os.path.abspath(template_path)

    content_tree = os.listdir(dir_path_content)
    for entry in content_tree:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry):
            shutil.copy(entry_path, dest_path)
        elif os.path.isdir(entry):