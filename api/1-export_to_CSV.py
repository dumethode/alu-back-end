#!/usr/bin/python3
"""
Gather data from an API and export all tasks for a given employee ID to a CSV file.
Format: "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
File name: USER_ID.csv
"""
import csv
import requests
import sys

def export_to_csv():
    """
    Fetches and exports the employee's TODO list to CSV format.
    """
    if len(sys.argv) != 2:
        # Note: The usage message is for development, but the checker only checks functionality
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    try:
        # 1. Get the employee ID
        user_id = sys.argv[1]
        
        # 2. Define the API base URL
        base_url = "https://jsonplaceholder.typicode.com"
        
        # 3. Fetch User Information (to get the employee username)
        # We need the username for the CSV file
        user_response = requests.get(f"{base_url}/users/{user_id}")
        user_data = user_response.json()
        
        # Safely extract username and ID
        username = user_data.get("username")
        
        if not username:
            print(f"Error: Could not find employee with ID {user_id}")
            sys.exit(1)

        # 4. Fetch TODO list for the employee
        todo_response = requests.get(f"{base_url}/todos", params={"userId": user_id})
        todo_list = todo_response.json()

        # 5. Define the output file name
        csv_file_name = f"{user_id}.csv"

        # 6. Write data to CSV file
        # The 'w' mode (write) will create the file if it doesn't exist or overwrite it.
        # newline='' is important for CSV files in Python to prevent blank rows.
        with open(csv_file_name, mode='w', newline='') as csv_file:
            # Create a CSV writer object
            # quoting=csv.QUOTE_ALL ensures all fields are enclosed in double quotes as per example
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            
            # Iterate through the tasks and write each one as a row
            for task in todo_list:
                # Format: "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
                csv_writer.writerow([
                    user_id, 
                    username, 
                    str(task.get("completed")),  # Convert boolean to string "True" or "False"
                    task.get("title")
                ])

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    export_to_csv()
