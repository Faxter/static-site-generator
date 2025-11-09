from src.htmlnode import HTMLNode
from src.leafnode import LeafNode, text_node_to_html_node
from src.parentnode import ParentNode
from src.textblock import (
    BlockType,
    block_to_block_type,
    code_block_to_lines,
    heading_block_to_line,
    markdown_to_text_blocks,
    ordered_list_block_to_lines,
    paragraph_block_to_line,
    quote_block_to_line,
    unordered_list_block_to_lines,
)
from src.textnode import markdown_text_to_textnodes


def markdown_to_html_node(document: str):
    blocks = markdown_to_text_blocks(document)
    children: list[HTMLNode] = []
    for block in blocks:
        node = text_block_to_html_node(block)
        children.append(node)
    return ParentNode("div", children)


def text_block_to_html_node(block: str) -> HTMLNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            line = paragraph_block_to_line(block)
            nodes = markdown_text_to_textnodes(line)
            children = []
            for node in nodes:
                children.append(text_node_to_html_node(node))
            return ParentNode("p", children)
        case BlockType.QUOTE:
            lines = quote_block_to_line(block)
            line = "<br />".join(lines)
            return LeafNode(line, "blockquote")
        case BlockType.UNORDERED_LIST:
            lines = unordered_list_block_to_lines(block)
            return ParentNode("ul", list_items_to_children_nodes(lines))
        case BlockType.ORDERED_LIST:
            lines = ordered_list_block_to_lines(block)
            return ParentNode("ol", list_items_to_children_nodes(lines))
        case BlockType.CODE:
            line = code_block_to_lines(block)
            return ParentNode("pre", [LeafNode(line, "code")])
        case BlockType.HEADING:
            heading_rank, heading_text = heading_block_to_line(block)
            return LeafNode(heading_text, f"h{heading_rank}")


def list_items_to_children_nodes(lines: list[str]):
    children: list[HTMLNode] = []
    for line in lines:
        sub_nodes = markdown_text_to_textnodes(line)
        sub_html_nodes = map(text_node_to_html_node, sub_nodes)
        children.append(ParentNode("li", list(sub_html_nodes)))
    return children
