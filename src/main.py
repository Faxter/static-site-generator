import os
import shutil
import sys
from pathlib import Path

from src.page_assembler import generate_page, insert_base_path

PATH_CONTENT = Path("content")
PATH_PUBLIC = Path("docs")
PATH_STATIC = Path("static")
PATH_TEMPLATE = Path("template.html")


def main():
    basepath = "/" if not sys.argv[1] else sys.argv[1]

    copy_contents(PATH_STATIC, PATH_PUBLIC)
    markdown = read_markdown_content(PATH_CONTENT)
    template = read_template_content(PATH_TEMPLATE)
    for path, content in markdown.items():
        print(f"Generating page from {path} using {PATH_TEMPLATE}")
        html = generate_page(content, template)
        html = insert_base_path(basepath, html)
        write_html(html, path, PATH_PUBLIC)


def copy_contents(src: Path, dst: Path):
    if not os.path.exists(src):
        raise Exception(f"source path {src} does not exist")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        source = Path(os.path.join(src, item))
        target = Path(os.path.join(dst, item))
        if os.path.isfile(source):
            shutil.copy(source, target)
        else:
            copy_contents(source, target)


def read_markdown_content(content_directory: Path):
    if not os.path.exists(content_directory):
        raise Exception(f"source path {content_directory} does not exist")

    markdown: dict[Path, str] = {}
    for item in os.listdir(content_directory):
        inner_path = Path(os.path.join(content_directory, item))
        if inner_path.is_file() and inner_path.name.endswith(".md"):
            with open(inner_path, "r") as f:
                markdown[inner_path] = f.read()
        elif inner_path.is_dir():
            markdown = markdown | read_markdown_content(inner_path)
    return markdown


def read_template_content(template: Path):
    if not os.path.exists(template):
        raise Exception(f"template {template} does not exist")

    with open(template, "r") as f:
        return f.read()


def write_html(html: str, contentpath: Path, publish_dir: Path):
    # contentpath: content/blog/glorfindel.md
    # write to   : public/blog/glorfindel.html
    parts = list(contentpath.parts)
    parts[0] = str(publish_dir)
    internal_path = Path(*parts)
    os.makedirs(os.path.dirname(internal_path), exist_ok=True)
    with open(internal_path.with_suffix(".html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
