import re
from collections.abc import Callable
from enum import Enum
from typing import final, override


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


@final
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = ""):
        self.text = text
        self.text_type = text_type
        self.url = url

    @override
    def __eq__(self, other: object):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    @override
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"


def markdown_text_to_textnodes(text: str):
    node = TextNode(text, TextType.PLAIN)
    bolded = split_text_nodes_by_bold_sections([node])
    italicized = split_text_nodes_by_italic_sections(bolded)
    coded = split_text_nodes_by_code_sections(italicized)
    images = split_text_nodes_by_image(coded)
    return split_text_nodes_by_links(images)


def split_text_nodes_by_bold_sections(old_nodes: list[TextNode]):
    return split_text_nodes_by_delimiter(old_nodes, "**", TextType.BOLD)


def split_text_nodes_by_italic_sections(old_nodes: list[TextNode]):
    return split_text_nodes_by_delimiter(old_nodes, "_", TextType.ITALIC)


def split_text_nodes_by_code_sections(old_nodes: list[TextNode]):
    return split_text_nodes_by_delimiter(old_nodes, "`", TextType.CODE)


def split_text_nodes_by_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    if not delimiter:
        return old_nodes
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise Exception(f"unmatched delimiter {delimiter} in text {node.text}")
        for i in range(len(splits)):
            if not splits[i]:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splits[i], TextType.PLAIN))
            else:
                new_nodes.append(TextNode(splits[i], text_type))
    return new_nodes


def split_text_nodes_by_image(old_nodes: list[TextNode]):
    return split_text_nodes_by_type(
        old_nodes, TextType.IMAGE, extract_markdown_images, "![{0}]({1})"
    )


def split_text_nodes_by_links(old_nodes: list[TextNode]):
    return split_text_nodes_by_type(
        old_nodes, TextType.LINK, extract_markdown_links, "[{0}]({1})"
    )


def extract_markdown_images(text: str):
    matcher = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"  # match for ![alt-text](link-to-image)
    return re.findall(matcher, text)


def extract_markdown_links(text: str):
    matcher = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"  # match for [link-text](link-url)
    return re.findall(matcher, text)


def split_text_nodes_by_type(
    old_nodes: list[TextNode],
    type: TextType,
    extract_function: Callable[[str], list[str]],
    format_str: str,
):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        elements = extract_function(node.text)
        if not elements:
            new_nodes.append(node)
            continue
        search_text = node.text
        for element in elements:
            element_text, element_url = element
            split_marker = format_str.format(element_text, element_url)
            split_text = search_text.split(split_marker, 1)
            search_text = split_text[1]
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
            new_nodes.append(TextNode(element_text, type, element_url))
        if search_text:
            new_nodes.append(TextNode(search_text, TextType.PLAIN))
    return new_nodes
