from pydantic import BaseModel


class TestCase(BaseModel):
    title: str
    steps: list[str]
    expected_result: str


class TestSuite(BaseModel):
    name: str
    cases: list[TestCase]
