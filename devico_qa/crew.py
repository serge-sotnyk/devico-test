from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml

# Uncomment the following line to use an example of a custom tool
# from devico_qa.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


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

    @agent
    def senior_qa(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_qa'],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            verbose=True
        )

    @task
    def find_test_cases_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_test_cases_task'],
        )

    @task
    def fill_test_case_task(self) -> Task:
        return Task(
            config=self.tasks_config['fill_test_case_task'],
            output_file='report.md'
        )

    # @crew
    # def crew(self) -> Crew:
    #     """Creates the DevicoQa crew"""
    #     return Crew(
    #         agents=self.agents,  # Automatically created by the @agent decorator
    #         tasks=self.tasks,  # Automatically created by the @task decorator
    #         process=Process.sequential,
    #         verbose=True,
    #         # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
    #     )

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
