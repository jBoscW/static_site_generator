class HTMLNode:
    def __init__(self, tag= None, value=None, children = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return " " + props_str
    
    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"
    

class LeafNode(HTMLNode): 
    def __init__(self, tag, value, props = None): 
        super().__init__(tag, value, props = props)

    def to_html(self):
        if not self.value: 
            raise ValueError("all leaf nodes must have values")
        if not self.tag: 
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


