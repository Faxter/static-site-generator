from src.textnode import TextType, TextNode
from src.leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(text_node.text, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"alt": text_node.text, "img": text_node.url})


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
