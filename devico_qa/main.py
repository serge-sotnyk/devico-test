import os
import sys
from pathlib import Path
from typing import cast

from crewai import Crew
from dotenv import load_dotenv

from devico_qa.crew import DevicoQaCrew
from devico_qa.models import TestSuite, TestCase
from devico_qa.tools.utils import get_page_description, get_page_elements, get_page_html

load_dotenv()


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'AI LLMs'
#     }
#     DevicoQaCrew().crew().kickoff(inputs=inputs)

def print_usage_metrics(crew: Crew) -> tuple[int, int]|float:
    model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')
    if model_name == "gpt-4o-mini":
        costs = (0.15 * crew.usage_metrics.prompt_tokens +
                 0.6 *crew.usage_metrics.completion_tokens) / 1_000_000
    elif model_name == "gpt-4o":
        costs = (2.5 * crew.usage_metrics.prompt_tokens +
                 10 * crew.usage_metrics.completion_tokens) / 1_000_000
    else:
        costs = (2.5 * crew.usage_metrics.prompt_tokens,
                 10 * crew.usage_metrics.completion_tokens)
    if isinstance(costs, tuple):
        print(f"Total tokens: input={costs[0]:.4f}, output={costs[1]:.4f}")
    else:
        print(f"Total costs: ${costs:.4f}")
    return costs


def run(root_dir: str):
    """
    Run the testcases finder crew.
    """
    root_dir = Path(root_dir)
    inputs_doc_info = {
        "page_description": get_page_description(root_dir),
        "active_elements": get_page_elements(root_dir),
        "simplified_html": get_page_html(root_dir),
    }

    # Run the testcases finder crew.
    investigate_crew = DevicoQaCrew().testcases_finder_crew()
    result = investigate_crew.kickoff(inputs=inputs_doc_info)
    # Usage metrics and costs
    cost = print_usage_metrics(investigate_crew)

    # Iterate with fill_test_case_crew
    fill_test_case_crew = DevicoQaCrew().testcase_filler_crew()
    res_as_obj: TestSuite = cast(TestSuite, result.pydantic)
    with open("testcases_stage_1.json", "wt", encoding="utf-8") as f:
        f.write(res_as_obj.model_dump_json(indent=2))

    # final_res = TestSuite(
    #     name=res_as_obj.name,
    # )
    #
    # for tc in res_as_obj.testcases:
    #     tc_inputs = {
    #         **inputs_doc_info,
    #         "testcase_object": tc.model_dump()
    #     }
    #     res = fill_test_case_crew.kickoff(inputs=tc_inputs)
    #     final_res.testcases.append(cast(TestCase, res.pydantic))
    #
    # with open("testcases.json", "wt", encoding="utf-8") as f:
    #     f.write(final_res.model_dump_json(indent=2))
    #
    # # Usage metrics and costs
    # cost_2 = print_usage_metrics(fill_test_case_crew)
    # if isinstance(cost, tuple):
    #     cost = (cost[0] + cost_2[0], cost[1] + cost_2[1])
    #     print(f"Total tokens: {cost}")
    # else:
    #     cost = cost + cost_2
    #     print(f"Total costs: ${cost:.4f}")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python main.py <root_dir>")
        sys.exit(1)
    run(sys.argv[1])
