from src.leafnode import LeafNode, text_node_to_html_node
from src.parentnode import ParentNode
from src.textblock import BlockType, block_to_block_type, block_to_line
from src.textnode import markdown_text_to_textnodes


def text_block_to_html_node(block: str):
    parent_node = ParentNode("div", [])
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            line = block_to_line(block, BlockType.PARAGRAPH)
            nodes = markdown_text_to_textnodes(line)
            children = []
            for node in nodes:
                children.append(text_node_to_html_node(node))
            parent_node.children.append(ParentNode("p", children))
        case BlockType.QUOTE:
            line = block_to_line(block, BlockType.QUOTE)
            parent_node.children.append(LeafNode(line, "blockquote"))
        case BlockType.UNORDERED_LIST:
            lines = block_to_line(block, BlockType.UNORDERED_LIST)
            children = []
            for line in lines:
                children.append(LeafNode(line, "li"))
            parent_node.children.append(ParentNode("ul", children))
        case BlockType.ORDERED_LIST:
            lines = block_to_line(block, BlockType.ORDERED_LIST)
            children = []
            for line in lines:
                children.append(LeafNode(line, "li"))
            parent_node.children.append(ParentNode("ol", children))
        case BlockType.CODE:
            line = block_to_line(block, BlockType.CODE)
            parent_node.children.append(ParentNode("pre", [LeafNode(line, "code")]))
        case BlockType.HEADING:
            line = block_to_line(block, BlockType.HEADING)
            parent_node.children.append(LeafNode(line[1], f"h{len(line[0])}"))

    return parent_node
