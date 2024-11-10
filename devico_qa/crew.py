import os
from pathlib import Path

import yaml
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from devico_qa.models import TestSuite, TestCase


@CrewBase
class DevicoQaCrew:
    """DevicoQa crew"""

    def __init__(self):
        """Initialize the crew with configuration from YAML files"""
        config_dir = Path(__file__).parent / "config"

        # Load agents configuration
        with open(config_dir / "agents.yaml", "r") as f:
            self.agents_config = yaml.safe_load(f)

        # Load tasks configuration    
        with open(config_dir / "tasks.yaml", "r") as f:
            self.tasks_config = yaml.safe_load(f)

        self.llm = LLM(model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini'), temperature=0.2)

    @agent
    def senior_qa(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['senior_qa'],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            verbose=True
        )

    @task
    def find_test_cases_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_test_cases_task'],
            output_pydantic=TestSuite,
        )

    @task
    def fill_test_case_task(self) -> Task:
        return Task(
            config=self.tasks_config['fill_test_case_task'],
            output_pydantic=TestCase,
        )

    @crew
    def testcases_finder_crew(self) -> Crew:
        """Creates the crew that finds test cases for the passed string"""
        return Crew(
            agents=[self.senior_qa()],
            tasks=[self.find_test_cases_task()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def testcase_filler_crew(self) -> Crew:
        """Creates the crew that fills testcases for the passed description"""
        return Crew(
            agents=[self.senior_qa()],
            tasks=[self.fill_test_case_task()],
            process=Process.sequential,
            verbose=True,
        )
