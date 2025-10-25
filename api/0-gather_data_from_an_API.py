#!/usr/bin/python3
"""
Script that fetches TODO list progress for a given employee ID from an API
"""
import requests
import sys


if __name__ == "__main__":
    employee_id = sys.argv[1]
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user data
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)
    user_data = user_response.json()
    employee_name = user_data.get("name")

    # Fetch todos for the user
    todos_url = "{}/todos?userId={}".format(base_url, employee_id)
    todos_response = requests.get(todos_url)
    todos = todos_response.json()

    # Calculate completed tasks
    completed_tasks = []
    for task in todos:
        if task.get("completed") is True:
            completed_tasks.append(task)

    total_tasks = len(todos)
    num_completed = len(completed_tasks)

    # Print results
    print("Employee {} is done with tasks({}/{}):".format(
        employee_name, num_completed, total_tasks))

    for task in completed_tasks:
        print("\t {}".format(task.get('title')))
