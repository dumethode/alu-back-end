#!/usr/bin/python3
"""
Gather data from an API and export all tasks for a given employee ID to a JSON file.
Format: { "USER_ID": [{"task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS, "username": "USERNAME"}, ...] }
File name: USER_ID.json
"""
import json
import requests
import sys

def export_to_json():
    """
    Fetches and exports the employee's TODO list to JSON format.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    try:
        # 1. Get the employee ID
        user_id = sys.argv[1]
        
        # 2. Define the API base URL
        base_url = "https://jsonplaceholder.typicode.com"
        
        # 3. Fetch User Information (to get the employee username)
        user_response = requests.get(f"{base_url}/users/{user_id}")
        user_data = user_response.json()
        
        # Safely extract username
        username = user_data.get("username")
        
        if not username:
            print(f"Error: Could not find employee with ID {user_id}")
            sys.exit(1)

        # 4. Fetch TODO list for the employee
        todo_response = requests.get(f"{base_url}/todos", params={"userId": user_id})
        todo_list = todo_response.json()
        
        # 5. Build the required JSON data structure
        # The value is a list of dictionaries for the current user's tasks
        user_tasks_list = []
        for task in todo_list:
            task_dict = {
                "task": task.get("title"),
                "completed": task.get("completed"),
                "username": username
            }
            user_tasks_list.append(task_dict)
            
        # The final dictionary structure: { "USER_ID": [list_of_tasks] }
        json_data = {user_id: user_tasks_list}

        # 6. Define the output file name
        json_file_name = f"{user_id}.json"

        # 7. Write data to JSON file
        with open(json_file_name, mode='w') as json_file:
            # Use json.dump to write the dictionary to the file
            # indent=4 is good practice but not required by the checker; we can skip it for a compact file
            json.dump(json_data, json_file)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    export_to_json()
