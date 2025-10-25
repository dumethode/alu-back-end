#!/usr/bin/python3
"""
Gather data from an API and display an employee's TODO list progress.
"""
import requests
import sys


def gather_data():
    """
    Fetches and displays the employee's TODO list progress.
    """
    if len(sys.argv) != 2:
        sys.exit(1)

    try:
        # 1. Get the employee ID
        user_id = sys.argv[1]
        base_url = "https://jsonplaceholder.typicode.com"

        # 2. Fetch User Information
        user_response = requests.get(f"{base_url}/users/{user_id}")
        user_data = user_response.json()
        
        # *** FIX 1: Strip Name Whitespace ***
        employee_name = user_data.get("name").strip()

        # 3. Fetch TODO list (PEP8 E128 compliant)
        todo_response = requests.get(
            f"{base_url}/todos",
            params={"userId": user_id}
        )
        todo_list = todo_response.json()

        # 4. Calculate task progress
        total_tasks = len(todo_list)
        done_tasks = [task.get("title")
                      for task in todo_list if task.get("completed") is True]
        number_of_done_tasks = len(done_tasks)

        # 5. Display the progress (*** FIX 2: Strict First Line Format ***)
        # The expected output is: Employee NAME is done with tasks(DONE/TOTAL):
        print("Employee {} is done with tasks({}/{}):".format(
            employee_name, number_of_done_tasks, total_tasks
        ))

        # 6. Display completed task titles (*** FIX 3: Strict Task Indentation ***)
        # Ensures exactly one tab (\t) and one space before the title.
        for task_title in done_tasks:
            # We strip the task title as well, just in case the API data has trailing/leading spaces
            print("\t {}".format(task_title.strip()))

    except Exception:
        # Catch all errors (API connection, bad ID) and exit as required
        sys.exit(1)


if __name__ == "__main__":
    gather_data()
