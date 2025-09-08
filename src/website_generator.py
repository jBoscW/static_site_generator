import os
import shutil
import src.blocks as blocks

def delete_and_move(public_dir, static_dir, deleted=False): 
    public_abspath = os.path.abspath(public_dir)
    static_abspath = os.path.abspath(static_dir)
    if not os.path.exists(static_abspath):
        raise ValueError("static directory does not exist")
    
    if deleted == False:
        print(f"deleting {public_dir} and contents: {os.listdir(public_abspath)}")
        shutil.rmtree(public_abspath)
        deleted = True
        print(f"creating {public_dir}")
        os.mkdir(public_abspath)
    
    static_tree = os.listdir(static_abspath)
    for item in static_tree: 
        print(item)
        item_abspath = os.path.join(static_abspath, item)
        public_new_abspath = os.path.join(public_abspath, item)
        if os.path.isfile(item_abspath):
            shutil.copy(item_abspath, public_abspath)
        elif os.path.isdir(item_abspath):
            os.mkdir(public_new_abspath)
            delete_and_move(public_new_abspath, item_abspath, deleted=True)

def extract_title(markdown): 
    markdown = markdown.strip().split('\n')
    for line in markdown:
        line = line.strip()
        if line.startswith('# '):
            return line.lstrip('#').strip()
        
    raise Exception("Title must start with '# '")

def generate_page(from_path, template_path, dest_path): 
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
    

