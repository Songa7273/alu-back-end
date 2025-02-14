#!/usr/bin/python3
"""
Script to gather employee TODO list progress from a REST API
"""
import requests
import sys

def get_employee_todo_progress(employee_id):
    """
    Retrieves and displays the TODO list progress for a specific employee
    Args:
        employee_id (int): The ID of the employee
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Get employee information
    employee_url = f"{base_url}/users/{employee_id}"
    try:
        employee_response = requests.get(employee_url)
        employee_response.raise_for_status()
        employee = employee_response.json()
        
        # Get todos for the employee
        todos_url = f"{base_url}/todos?userId={employee_id}"
        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos = todos_response.json()
        
        # Calculate progress
        total_tasks = len(todos)
        done_tasks = sum(1 for todo in todos if todo['completed'])
        
        # Display progress
        print(f"Employee {employee['name']} is done with tasks({done_tasks}/{total_tasks}):")
        
        # Display completed tasks
        for todo in todos:
            if todo['completed']:
                print(f"\t {todo['title']}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch data from API: {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid data received from API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>", 
              file=sys.stderr)
        sys.exit(1)
    
    try:
        employee_id = int(sys.argv[1])
        if employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    get_employee_todo_progress(employee_id)
