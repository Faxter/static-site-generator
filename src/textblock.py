from enum import Enum
from functools import reduce
from re import DOTALL, search


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_text_blocks(document: str):
    blocks: list[str] = document.split("\n\n")
    return list(map(str.strip, filter(None, blocks)))


def block_to_block_type(block: str) -> BlockType:
    heading_matcher = r"^#{1,6} .*"
    code_matcher = r"^`{3}.*`{3}$"
    ordered_list_matcher = r"^\d\. .*$"
    if search(heading_matcher, block):
        return BlockType.HEADING
    if search(code_matcher, block, DOTALL):
        return BlockType.CODE
    lines = block.split("\n")
    if reduce(lambda acc, s: acc and s.startswith(">"), lines, True):
        return BlockType.QUOTE
    if reduce(lambda acc, s: acc and s.startswith("- "), lines, True):
        return BlockType.UNORDERED_LIST
    if reduce(lambda acc, s: acc and search(ordered_list_matcher, s), lines, True):
        for i in range(len(lines)):
            if not lines[i].startswith(str(i + 1)):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_line(block: str, type: BlockType):
    lines = block.split("\n")
    match type:
        case BlockType.PARAGRAPH:
            pass
        case BlockType.QUOTE:
            lines = list(map(lambda s: s[2:], lines))
            return " ".join(lines) if len(lines) > 1 else " ".join(lines)
        case BlockType.UNORDERED_LIST:
            return list(map(lambda s: s[2:], lines))
        case BlockType.ORDERED_LIST:
            return list(map(lambda s: s[3:], lines))
        case BlockType.CODE:
            return block[3:-3]
        case BlockType.HEADING:
            heading_matcher = r"^(#{1,6}) (.*)"
            m = search(heading_matcher, block)
            return [m.group(1), m.group(2)]

    return " ".join(lines)
