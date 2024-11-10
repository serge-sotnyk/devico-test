from abc import ABC
from pathlib import Path

from crewai_tools import BaseTool


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

class ToolLinkedToDir(BaseTool, ABC):
    root_dir: Path


class GetPageDescription(ToolLinkedToDir):
    name: str = "page_description"
    description: str = (
        "Return the plain-text description of the page."
    )

    # args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self) -> str:
        # read page_description.txt from self.root_dir folder
        try:
            return (self.root_dir / "page_description.txt").read_text(encoding="utf-8")
        except Exception as ex:
            return "Error: " + str(ex)


class GetPageHtml(ToolLinkedToDir):
    name: str = "page_html"
    description: str = (
        "Return the simplified HTML of the page."
    )

    # args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self) -> str:
        # find the first .html file in self.root_dir folder and return its content
        try:
            first_html_file = next(self.root_dir.glob("*.html"), None)
            return first_html_file.read_text(encoding="utf-8") if first_html_file \
                else "Error: No .html file found!"
        except Exception as ex:
            return "Error: " + str(ex)


class GetPageElements(ToolLinkedToDir):
    name: str = "page_elements"
    description: str = (
        "Return the JSON with list of active elements of the page."
    )

    def _run(self) -> str:
        # find the first .json file in self.root_dir folder and return its content
        try:
            first_json_file = next(self.root_dir.glob("*.json"), None)
            return first_json_file.read_text(encoding="utf-8") if first_json_file \
                else "Error: No .json file found!"
        except Exception as ex:
            return "Error: " + str(ex)
