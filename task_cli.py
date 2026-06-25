import argparse
import json
import os
import time

TASK_FILE = "tasks.json"

# Task status constants to avoid typos
TODO = "todo"
IN_PROGRESS = "in-progress"
DONE = "done"


def load_data():
    """
    Load tasks from the JSON file.
    Returns an empty list if the file does not exist or is invalid.
    """
    if os.path.exists(TASK_FILE) and os.path.getsize(TASK_FILE) > 0:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    return []


def save_data(data):
    """Persist all tasks to disk."""
    with open(TASK_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_next_id():
    """Generate the next available task ID."""
    data = load_data()

    current_id = 0

    for task in data:
        current_id = max(current_id, task["id"])

    return current_id + 1


def update_status(task_id, status):
    """Update the status of a task."""
    data = load_data()

    for task in data:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = time.ctime()

            save_data(data)

            print(f"Task status changed to '{status}'")
            return

    print(f"Task with ID {task_id} not found")


def main():
    parser = argparse.ArgumentParser(
        description="Simple command line task tracker"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # ---------------- Add command ----------------
    add_parser = subparsers.add_parser(
        "add",
        help="Create a new task"
    )
    add_parser.add_argument(
        "description",
        help="Description of the task"
    )

    # ---------------- Update command ----------------
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing task"
    )
    update_parser.add_argument(
        "id",
        type=int,
        help="Task ID"
    )
    update_parser.add_argument(
        "description",
        help="New task description"
    )

    # ---------------- Delete command ----------------
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task"
    )
    delete_parser.add_argument(
        "id",
        type=int,
        help="Task ID"
    )

    # ---------------- Status commands ----------------
    mark_in_progress_parser = subparsers.add_parser(
        "mark-in-progress",
        help="Mark task as in progress"
    )
    mark_in_progress_parser.add_argument(
        "id",
        type=int,
        help="Task ID"
    )

    mark_done_parser = subparsers.add_parser(
        "mark-done",
        help="Mark task as done"
    )
    mark_done_parser.add_argument(
        "id",
        type=int,
        help="Task ID"
    )

    # ---------------- List command ----------------
    list_parser = subparsers.add_parser(
        "list",
        help="List tasks"
    )

    # Optional positional argument:
    # task-cli list
    # task-cli list done
    list_parser.add_argument(
        "status",
        nargs="?",
        default=None,
        help="Filter tasks by status"
    )

    args = parser.parse_args()

    # ================= ADD =================
    if args.command == "add":
        current_time = time.ctime()

        new_task = {
            "id": get_next_id(),
            "description": args.description,
            "status": TODO,
            "createdAt": current_time,
            "updatedAt": current_time
        }

        data = load_data()
        data.append(new_task)
        save_data(data)

        print(f"Task added successfully (ID: {new_task['id']})")

    # ================= UPDATE =================
    elif args.command == "update":
        data = load_data()

        for task in data:
            if task["id"] == args.id:
                task["description"] = args.description
                task["updatedAt"] = time.ctime()

                save_data(data)

                print(f"Task updated successfully (ID: {args.id})")
                return

        print(f"Task with ID {args.id} not found")

    # ================= DELETE =================
    elif args.command == "delete":
        data = load_data()

        updated_data = [
            task for task in data
            if task["id"] != args.id
        ]

        if len(updated_data) == len(data):
            print(f"Task with ID {args.id} not found")
        else:
            save_data(updated_data)
            print(f"Task deleted successfully (ID: {args.id})")

    # ================= STATUS CHANGES =================
    elif args.command == "mark-in-progress":
        update_status(args.id, IN_PROGRESS)

    elif args.command == "mark-done":
        update_status(args.id, DONE)

    # ================= LIST =================
    elif args.command == "list":
        data = load_data()

        # Apply filter only if user supplied a status
        if args.status:
            data = [
                task for task in data
                if task["status"] == args.status
            ]

        if not data:
            print("No tasks found")
            return

        for task in data:
            print(
                f"[{task['id']}] "
                f"{task['description']} "
                f"({task['status']})"
            )


if __name__ == "__main__":
    main()