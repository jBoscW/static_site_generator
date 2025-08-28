class HTMLNode:
    def __init__(self, tag= None, value=None, children = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return " " + props_str
    
    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"
    

class LeafNode(HTMLNode): 
    def __init__(self, tag, value, props = None): 
        super().__init__(tag, value, props = props)

    def to_html(self):
        if self.value is None: 
            raise ValueError("all leaf nodes must have values")
        if self.tag is None: 
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        # raise ValueError("All parent nodes must have a tag.")
        if self.tag is None: 
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("The parent node must have children.")
        
        text = ""
        for node in self.children: 
            text += node.to_html()
            
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"
