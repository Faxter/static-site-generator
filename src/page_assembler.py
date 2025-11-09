from pathlib import Path
from re import match

from src.node_assembler import markdown_to_html_node


def generate_page(source: Path, template: Path):
    print(f"Generating page from {source} using {template}")
    markdown = ""
    template_content = ""
    with open(source, "r") as f:
        markdown = f.read()
    with open(template, "r") as f:
        template_content = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title_from_markdown(markdown)
    result = template_content.replace(r"{{ Title }}", title)
    result = result.replace(r"{{ Content }}", html)
    return result


def extract_title_from_markdown(document: str):
    heading_1_matcher = r"^# (.*)"
    m = match(heading_1_matcher, document)
    if not m:
        raise Exception("could not find a header of rank 1 in the document!")
    return str(m.group(1))
