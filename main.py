import argparse
import json
import os
import time

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

def update_status(task_id,status):
    data=load_data()
    for task in data:
        if task["id"]==task_id:
            task["status"]=status
            task["updatedAt"]=time.ctime()
            save_data(data)
            return
    print("Task not found")

def main():
    parser = argparse.ArgumentParser(description="Store user info into Json")
    
    subparsers=parser.add_subparsers(dest="command",required=True)
    add_parser = subparsers.add_parser("add",help="create new task")
    update_parser = subparsers.add_parser("update", help = "update existing task")
    delete_parser = subparsers.add_parser("delete", help = "delete existing task")
    mark_inprogress_parser= subparsers.add_parser("mark-in-progress", help = "change the state of task")
    mark_done_parser= subparsers.add_parser("mark-done", help = "change the state of task")    
    list_parser= subparsers.add_parser("list", help = "List the task as per demand")
    #add parser
    add_parser.add_argument("description", help="description of the new task")
    #update parser
    update_parser.add_argument("id",type=int,help="task id which needs update")
    update_parser.add_argument("description", help="updated description for the task")
    #delete pareser
    delete_parser.add_argument("id",type=int,help="task id which needs delete")
    # parmark_inprogress_parser
    mark_inprogress_parser.add_argument("id",type=int,help="task id which needs to move to inprogress")
    #mark
    mark_done_parser.add_argument("id",type=int,help="task id which needs to move to done")
    # list 
    list_parser.add_argument("status", help="status of the task")

    args=parser.parse_args()

    if args.command=="add":
        current_time=time.ctime()
        new_entry={
            "id":get_next_id(),
            "description":args.description,
            "status":"todo",
            "createdAt": time.ctime(),
            "updatedAt":time.ctime()
        }
        data=load_data()
        data.append(new_entry)
        save_data(data)
        print(f"Task added successfully (ID: {new_entry['id']})")


    if args.command=="update":
        data=load_data()
        found = False
        for task in data:
            if task.get('id')==args.id:
                found=True
                task['description']=args.description
                task['updatedAt']=time.ctime()
                break
        if found:
            save_data(data)
            print("# Output: Task updated successfully (ID:{args.id})")
        else :
            print("# Output: Task is not present {args.id})")

    if args.command=="delete":
        data=load_data()
        updated_data = [task for task in data if task.get('id')!=args.id]
        if len(data)==len(updated_data):
            print("not found")
        else:
            save_data(updated_data)
            print("# Output: Task deleted successfully (ID:{args.id})")
    
    if args.command=="mark-in-progress":
        data=load_data()
        for task in data:
            if(task['id']==args.id):
                task['status']='in-progress'
                task['updatedAt']=time.ctime()
        save_data(data)
    
    if args.command=="mark-done":
        data=load_data()
        for task in data:
            if(task['id']==args.id):
                task['status']='done'
                task['updatedAt']=time.ctime()
        save_data(data)

    if args.command=="list" and args.status ==None:
        data=load_data()
        for task in data:
            print(task)
    
    if args.command=="list" and args.status != None:
        data=load_data()
        to_show_task = [task for task in data if task.get('status')==args.status]
        for t in to_show_task:
            print(t)
    

if __name__=="__main__":
    main()