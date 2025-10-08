from textnode import TextNode, TextType


def main():
    node = TextNode("some cool text", TextType.LINK, "https://faxxter.com")
    print(node)


if __name__ == "__main__":
    main()
