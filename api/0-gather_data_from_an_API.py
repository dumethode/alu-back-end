#!/usr/bin/python3
"""Fetch and display user TODO progress"""

import requests
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ./script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    user_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    todos_url = f"https://jsonplaceholder.typicode.com/users/{user_id}/todos"

    user_res = requests.get(user_url)
    todos_res = requests.get(todos_url)

    if user_res.status_code != 200:
        print("Error: user not found")
        sys.exit(1)

    user_info = user_res.json()
    todos_info = todos_res.json()

    employee_name = user_info.get("name", "Unknown")
    completed_tasks = [t for t in todos_info if t.get("completed")]
    total_number_of_tasks = len(todos_info)
    number_of_done_tasks = len(completed_tasks)

    print("Employee {} is done with tasks({}/{}):".
          format(employee_name, number_of_done_tasks, total_number_of_tasks))

    for task in completed_tasks:
        print(f"\t {task['title']}")
