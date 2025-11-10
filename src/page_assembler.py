from re import match

from src.node_assembler import markdown_to_html_node


def generate_page(markdown: str, template: str):
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title_from_markdown(markdown)
    result = template.replace(r"{{ Title }}", title)
    result = result.replace(r"{{ Content }}", html)
    return result


def insert_base_path(basepath: str, html: str):
    result = html.replace('href="/', f'href="{basepath}')
    return result.replace('src="/', f'src="{basepath}')


def extract_title_from_markdown(document: str):
    heading_1_matcher = r"^# (.*)"
    m = match(heading_1_matcher, document)
    if not m:
        raise Exception("could not find a header of rank 1 in the document!")
    return str(m.group(1))
