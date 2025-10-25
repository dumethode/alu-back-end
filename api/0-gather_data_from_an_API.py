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
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        # 1. Get the employee ID from the command line argument
        user_id = sys.argv[1]
        base_url = "https://jsonplaceholder.typicode.com"

        # 2. Fetch User Information (to get the employee name)
        user_response = requests.get(f"{base_url}/users/{user_id}")
        user_data = user_response.json()

        # Safely extract the employee name using .get()
        employee_name = user_data.get("name")

        if not employee_name:
            print(f"Error: Could not find employee with ID {user_id}")
            sys.exit(1)

        # 3. Fetch TODO list for the employee
        todo_response = requests.get(f"{base_url}/todos",
                                    params={"userId": user_id})
        todo_list = todo_response.json()

        # 4. Calculate task progress
        total_tasks = len(todo_list)
        done_tasks = [task.get("title")
                      for task in todo_list if task.get("completed") is True]
        number_of_done_tasks = len(done_tasks)

        # 5. Display the progress
        print(f"Employee {employee_name} is done with tasks"
              f"({number_of_done_tasks}/{total_tasks}):")

        # 6. Display the completed task titles with the required indentation
        for task_title in done_tasks:
            print(f"\t {task_title}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        sys.exit(1)
    except ValueError:
        print("Error: Employee ID must be an integer.")
        sys.exit(1)


if __name__ == "__main__":
    gather_data()
