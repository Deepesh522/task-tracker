import argparse
import json
import os

TASK_SHEET="task.json"


def load_data():
    if os.path.exists(TASK_SHEET) and os.path.getsize(TASK_SHEET) > 0:
        with open(TASK_SHEET, "r") as f:
            try:
                data=json.load(f)
            except json.JSONDecodeError:
                data=[]
    else:
        data=[]
    return data

def get_next_id():
    data = load_data()
    current = 0
    for task in data:
        task_id = task.get('id')
        if isinstance(task_id, int):
            current = max(current, task_id)
    return current + 1

def save_data(data):
    with open(TASK_SHEET,"w") as file:
        json.dump(data,file,indent=4)

def main():
    parser = argparse.ArgumentParser(description="Store user info into Json")
    
    subparsers=parser.add_subparsers(dest="command",required=True)
    add_parser = subparsers.add_parser("add",help="create new task")
    update_parser = subparsers.add_parser("update", help = "update existing task")
    delete_parser = subparsers.add_parser("delete", help = "delete existing task")
    mark_parser= subparsers.add_parser("mark", help = "change the state of task")
    list_parser= subparsers.add_parser("list", help = "List the task as per demand")
    #add parser
    add_parser.add_argument("description", help="description of the new task")
    #update parser
    update_parser.add_argument("id",type=int,help="task id which needs update")
    update_parser.add_argument("description", help="updated description for the task")
    #delete pareser
    delete_parser.add_argument("id",type=int,help="task id which needs delete")
    #mark parser
    mark_parser.add_argument

    args=parser.parse_args()

    if args.command=="add":
        new_entry={
            "id":get_next_id(),
            "description":args.description
        }
        data=load_data()
        data.append(new_entry)
        save_data(data)
        print("# Output: Task added successfully (ID: ",{new_entry['id']},")")


    if args.command=="update":
        data=load_data()
        for task in data:
            if task.get('id')==args.id:
                task['description']=args.description
        save_data(data)

    if args.command=="delete":
        data=load_data()
        updated_data = [task for task in data if task.get('id')!=args.id]
        if len(data)==len(updated_data):
            print("not found")
        save_data(updated_data)
    
    if args.command=="mark":




if __name__=="__main__":
    main()