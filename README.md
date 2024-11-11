# devico-test
Test task on DS/AI-dev position for Devico

# Installation

1. Install Python >=3.9 (or make sure it's already installed)
2. Clone the repository locally and navigate to it
3. Create a virtual environment
    ```bash
    python{your_python_version} -m venv venv
    ```
4. Activate the virtual environment
    Mac/Linux
    ```bash
    source venv/bin/activate
    ```
    or 
    Windows
    ```bash
    venv\Scripts\activate
    ```
5. Install the requirements
    ```bash
    pip install -r requirements.txt
    ```
6. Copy the `.env-example` to `.env` and add your API keys 
7. Run the script
    ```bash
    python main.py {directory_of_page}
    ```
    Pass as an argument the directory with the following information:
    * page_description.txt
    * *.html - simplified HTML of the page
    * *.json - list of active elements of the page
8. Find the result in the `testcases.json` file