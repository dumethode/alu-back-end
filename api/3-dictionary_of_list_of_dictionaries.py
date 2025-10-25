#!/usr/bin/python3
"""
Gather data from an API for all employees and export it to a single JSON file.
Format: { "USER_ID": [{"username": "USERNAME", "task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS}, ...] }
File name: todo_all_employees.json
"""
import json
import requests
import sys

def export_all_to_json():
    """
    Fetches and exports the TODO list for ALL employees to a single JSON file.
    """
    try:
        # 1. Define the API base URL
        base_url = "https://jsonplaceholder.typicode.com"
        
        # 2. Fetch ALL User Information
        users_response = requests.get(f"{base_url}/users")
        users_data = users_response.json()
        
        # 3. Fetch ALL TODO list items
        todos_response = requests.get(f"{base_url}/todos")
        todos_list = todos_response.json()

        # 4. Create a dictionary to map User ID to Username for easy lookup
        # { "1": "Bret", "2": "Antonette", ... }
        user_id_to_username = {}
        for user in users_data:
            user_id_to_username[str(user.get("id"))] = user.get("username")
            
        # 5. Build the final JSON data structure: { "USER_ID": [tasks_list] }
        # Initialize the master dictionary
        all_employee_data = {}
        
        # Iterate through all tasks and group them by user ID
        for task in todos_list:
            user_id = str(task.get("userId"))
            
            # Create the dictionary for the current task
            task_dict = {
                "username": user_id_to_username.get(user_id),
                "task": task.get("title"),
                "completed": task.get("completed")
            }
            
            # Add the task to the list for the correct user_id key
            # Use .get() to retrieve the list, or set a default empty list if the key is new
            if user_id not in all_employee_data:
                all_employee_data[user_id] = []
            
            all_employee_data[user_id].append(task_dict)

        # 6. Define the output file name
        json_file_name = "todo_all_employees.json"

        # 7. Write data to JSON file
        with open(json_file_name, mode='w') as json_file:
            json.dump(all_employee_data, json_file)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    export_all_to_json()
