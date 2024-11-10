from pathlib import Path


def get_page_description(root_dir: Path) -> str:
    """Return the plain-text description of the page."""
    return (root_dir / "page_description.txt").read_text(encoding="utf-8")


def get_page_html(root_dir: Path) -> str:
    """Return the simplified HTML of the page."""
    first_html_file = next(root_dir.glob("*.html"), None)
    if not first_html_file:
        raise FileNotFoundError("No .html file found!")
    return first_html_file.read_text(encoding="utf-8")


def get_page_elements(root_dir: Path) -> str:
    """Return the JSON with list of active elements of the page."""
    first_json_file = next(root_dir.glob("*.json"), None)
    if not first_json_file:
        raise FileNotFoundError("No .json file found!")
    return first_json_file.read_text(encoding="utf-8")
