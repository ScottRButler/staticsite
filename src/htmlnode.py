class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initializes an HTMLNode object.

        Args:
            tag (str, optional): The HTML tag name (e.g., 'p', 'a'). Defaults to None.
            value (str, optional): The text content of the node. Defaults to None.
            children (list[HTMLNode], optional): A list of child HTMLNode objects. Defaults to None.
            props (dict[str, str], optional): HTML attributes as key-value pairs. Defaults to None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the node to an HTML string.
        This base method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        """
        Converts the props dictionary into a string of HTML attributes.

        Returns:
            str: A string formatted as ' key1="value1" key2="value2"...',
                 or an empty string if no props exist.
        """
        if not self.props:
            return ""
        html_props = []
        for key, val in self.props.items():
            html_props.append(f'{key}="{val}"')
        # Important: Join with spaces and prepend a single leading space
        return " " + " ".join(html_props)

    def __repr__(self):
        """
        Returns a developer-friendly string representation of the HTMLNode.
        """
        return (f"HTMLNode(tag={self.tag}, value={self.value}, "
                f"children={self.children}, props={self.props})")
        
        
        


class LeafNode(HTMLNode):
    """
    Represents an HTML node with no children (a "leaf" in the HTML tree).
    Examples: <p>Text</p>, <a>Link</a>, <b>Bold</b>, raw text.
    """
    def __init__(self, value, tag=None, props=None):
        """
        Initializes a LeafNode.

        Args:
            value (str): The content of the node (e.g., text). This is required.
            tag (str, optional): The HTML tag name (e.g., 'p', 'a'). Defaults to None (raw text).
            props (dict[str, str], optional): HTML attributes. Defaults to None.

        Raises:
            ValueError: If value is None (implicitly handled by to_html check).
                        Note: The constructor itself doesn't prevent passing None,
                        but to_html will fail as required. Best practice might be
                        to check here, but following prompt structure.
        """
        # Call the parent constructor, explicitly setting children to None
        super().__init__(tag=tag, value=value, children=None, props=props)
        # Note: self.value = value is handled by super().__init__

    def to_html(self):
        """
        Renders the leaf node as an HTML string.

        Returns:
            str: The HTML representation of the node.

        Raises:
            ValueError: If the node's value is None.
        """
        # Rule 1: Raise ValueError if value is missing
        if self.value is None:
            # Although __init__ requires value, this check adheres to the specific
            # requirement for to_html to raise the error.
            raise ValueError("Invalid HTML: LeafNode requires a value.")

        # Rule 2: Return raw text if tag is None
        if self.tag is None:
            return self.value

        # Rule 3: Render with HTML tag
        # Get props string (e.g., ' href="..."') or empty string
        props_html = self.props_to_html()
        # Format: <tag props>value</tag>
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        # Optional: Provide a slightly more specific repr for LeafNode
        return (f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})")        
    
    

class ParentNode(HTMLNode):
    """
    Represents an HTML node that contains other HTML nodes (children).
    Examples: <div><span>...</span></div>, <p><b>Bold</b> text.</p>
    """
    def __init__(self, tag, children, props=None):
        """
        Initializes a ParentNode.

        Args:
            tag (str): The HTML tag name (e.g., 'p', 'div'). Required.
            children (list[HTMLNode]): A list of child HTMLNode objects. Required.
            props (dict[str, str], optional): HTML attributes. Defaults to None.

        Raises:
             # Note: Initial checks for tag/children being None are moved to to_html
             # as per prompt instructions, although checking here is often preferred.
        """
        # Call parent constructor, explicitly setting value to None
        super().__init__(tag=tag, value=None, children=children, props=props)
        # Note: self.tag, self.children, self.props assigned by super()

    def to_html(self):
        """
        Renders the parent node and its children as an HTML string recursively.

        Returns:
            str: The HTML representation of the node and its descendants.

        Raises:
            ValueError: If the node's tag is missing.
            ValueError: If the node's children list is missing (None).
                        An empty list [] is considered valid.
        """
        # Rule 1: Raise ValueError if tag is missing
        if not self.tag: # Checks for None or empty string
             raise ValueError("Invalid HTML: ParentNode requires a tag.")

        # Rule 2: Raise ValueError if children is None
        # Allow empty list self.children == []
        if self.children is None:
             raise ValueError("Invalid HTML: ParentNode requires children.")

        # Build the HTML string
        # Start with opening tag and props
        props_html = self.props_to_html() # Get attribute string or ""
        html_content = f"<{self.tag}{props_html}>"

        # Recursively call to_html on children and append
        for child in self.children:
            html_content += child.to_html()

        # Add closing tag
        html_content += f"</{self.tag}>"

        return html_content

    def __repr__(self):
        # Optional: Provide a specific repr for ParentNode
        return (f"ParentNode(tag={self.tag}, children={self.children}, "
                f"props={self.props})")