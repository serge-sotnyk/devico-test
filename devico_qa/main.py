import sys
from devico_qa.crew import DevicoQaCrew
from dotenv import load_dotenv

load_dotenv()


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    DevicoQaCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        DevicoQaCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2],
                                    inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DevicoQaCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        DevicoQaCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2],
                                   inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "train":
        train()
    elif sys.argv[1] == "replay":
        replay()
    elif sys.argv[1] == "test":
        test()
