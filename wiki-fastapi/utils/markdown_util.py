import markdown2


def markdown_to_html(content: str) -> str:

    """Convert Markdown content to HTML"""
    return markdown2.markdown(content)

