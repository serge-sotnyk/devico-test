from typing import Literal

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    title: str
    description: str
    steps: list[str] = Field(default_factory=list)
    expected_results: list[str] = Field(default_factory=list)
    priority: Literal["low", "medium", "high", ""] = ""


class TestSuite(BaseModel):
    name: str = "Test Suite"
    testcases: list[TestCase] = Field(default_factory=list)
