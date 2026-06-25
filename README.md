# https://roadmap.sh/projects/task-tracker

## For setup 
run these cli commands 
those are : 
```bat
git clone https://github.com/Deepesh522/task-tracker.git
```

```bat
cd task-tracker
```

```bat
pip install -e .
```
## For Testing 
### Show general help
```bat
task-cli --help
```
### Show help for a specific command
```bat
task-cli add --help
```
### List when there are no tasks
```bat
task-cli list
```
### Add some tasks
```bat
task-cli add "Buy groceries"
task-cli add "Go to gym"
task-cli add "Prepare Spring interview notes"
```
### List all tasks
```bat
task-cli list
```
### Filter by status
```bat
task-cli list todo
```
### Update an existing task
```bat
task-cli update 2 "Go to gym and do legs"
```
### Try updating a non-existent task
```bat
task-cli update 999 "This should fail"
```
### Mark tasks as in progress
```bat
task-cli mark-in-progress 1
task-cli mark-in-progress 2
```
### Verify filtering works
```bat
task-cli list in-progress
task-cli list todo
```
### Mark task as done
```bat
task-cli mark-done 1
```
### Verify status transition
```bat
task-cli list done
task-cli list in-progress
task-cli list todo
```
### Delete an existing task
```bat
task-cli delete 2
```
### Try deleting a non-existent task
```bat
task-cli delete 999
```
### Verify deletion
```bat
task-cli list
```
### Verify filters after deletion
```bat
task-cli list done
task-cli list in-progress
task-cli list todo
```
