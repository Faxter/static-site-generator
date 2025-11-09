import os
import shutil
from pathlib import Path

from src.page_assembler import generate_page


def main():
    copy_contents(Path("static"), Path("public"))
    html = generate_page(Path("content/index.md"), Path("template.html"))
    with open("public/index.html", "w") as f:
        f.write(html)


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


if __name__ == "__main__":
    main()
