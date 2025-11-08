from src.htmlnode import HTMLNode
from src.leafnode import LeafNode, text_node_to_html_node
from src.parentnode import ParentNode
from src.textblock import (
    BlockType,
    block_to_block_type,
    block_to_line,
    markdown_to_text_blocks,
)
from src.textnode import markdown_text_to_textnodes


def markdown_to_html_node(document: str):
    blocks = markdown_to_text_blocks(document)
    div_node = ParentNode("div", [])
    for block in blocks:
        node = text_block_to_html_node(block)
        div_node.children.append(node)
    return div_node


def text_block_to_html_node(block: str) -> HTMLNode:
    # parent_node = ParentNode("div", [])
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            line = block_to_line(block, BlockType.PARAGRAPH)
            nodes = markdown_text_to_textnodes(line)
            children = []
            for node in nodes:
                children.append(text_node_to_html_node(node))
            return ParentNode("p", children)
        case BlockType.QUOTE:
            line = block_to_line(block, BlockType.QUOTE)
            return LeafNode(line, "blockquote")
        case BlockType.UNORDERED_LIST:
            lines = block_to_line(block, BlockType.UNORDERED_LIST)
            children = []
            for line in lines:
                children.append(LeafNode(line, "li"))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            lines = block_to_line(block, BlockType.ORDERED_LIST)
            children = []
            for line in lines:
                children.append(LeafNode(line, "li"))
            return ParentNode("ol", children)
        case BlockType.CODE:
            line = block_to_line(block, BlockType.CODE)
            return ParentNode("pre", [LeafNode(line, "code")])
        case BlockType.HEADING:
            line = block_to_line(block, BlockType.HEADING)
            return LeafNode(line[1], f"h{len(line[0])}")
