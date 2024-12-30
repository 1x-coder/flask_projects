from flask import Flask, render_template, redirect, url_for, request
import sqlite3

dbName = "todo.db"

def make_db_connection():
    return sqlite3.connect(f"{dbName}")

def check_table_exists(tableName):
    db_con = make_db_connection()
    db_cur = db_con.cursor()
    listOfTables = db_cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';").fetchall()
    if listOfTables == []:
        db_con.close()
        return False
    else:
        db_con.close()     
        return True

if (not check_table_exists('tasks')):
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    query = """CREATE TABLE tasks (
  task_id INTEGER PRIMARY KEY,
  task_title VARCHAR(255) NOT NULL,
  task_description TEXT,
  order_index INTEGER DEFAULT 0,
  status VARCHAR(20) CHECK (status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
  parent_task_id INTEGER REFERENCES tasks(id),
  subtasks TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );"""
    
    dbCur.execute(query)
    dbCon.close()

def add_subtask():
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()

    query1 = """
        SELECT task_id, parent_task_id From tasks
        Order By task_id Desc LIMIT 1;
    """
    data = dbCur.execute(query1).fetchone()
    subtaskId = data[0]
    parentTaskId = data[1]

    query2 = f"Select subtasks From tasks Where task_id = {parentTaskId}"
    data = dbCur.execute(query2).fetchone()
    subtasks = data[0]

    if subtasks is None:
        query3 = f"UPDATE tasks SET subtasks = {subtaskId} WHERE task_id = {parentTaskId}"
    else:
        query3 = f"UPDATE tasks SET subtasks = {subtasks}{subtaskId} WHERE task_id = {parentTaskId}"

    dbCur.execute(query3)
    dbCon.commit()

    dbCon.close()

def find_subtasks_for_task(rootTask, subtasks):
    subtaskList = []
    for subtaskId in rootTask[6]:
        for subtask in subtasks:
            if subtask[0] == int(subtaskId):
                if subtask[6] is None:
                    subtaskList.append({"task_id": subtask[0], "task_title": subtask[1], "task_description": subtask[2], "status": subtask[4]})
                else:
                    nestedSubtaskList = find_subtasks_for_task(subtask, subtasks)
                    subtaskList.append({"task_id": subtask[0], "task_title": subtask[1], "task_description": subtask[2], "status": subtask[4], "subtasks": nestedSubtaskList})

    return subtaskList

app = Flask(__name__)

@app.route("/")
def index():
    query1 = "SELECT * FROM tasks WHERE parent_task_id is NULL"
    query2 = "SELECT * FROM tasks WHERE parent_task_id is NOT NULL"
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    rootTasks = dbCur.execute(query1).fetchall()
    subtasks = dbCur.execute(query2).fetchall()
    dbCon.commit()
    dbCon.close()
    taskList = []
    for task in rootTasks:
        if task[6] is None:
            taskList.append({"task_id": task[0], "task_title": task[1], "task_description": task[2], "status": task[4]})
        else:
            subtaskList = find_subtasks_for_task(task, subtasks)
            taskList.append({"task_id": task[0], "task_title": task[1], "task_description": task[2], "status": task[4], "subtasks": subtaskList})
    
    return render_template("index.html", data=taskList)

@app.route("/add", methods=['POST'])
def add_task():
    data = request.get_json()
    if data.get('task_title'):
        columns = "task_title"
        placeholders = "?"
        values = (data.get('task_title'),)

    if data.get('task_description'):
        columns += ", task_description"
        placeholders += ", ?"
        values += (data.get('task_description'),)
    
    if data.get('order_index'):
        columns += ", order_index"
        placeholders += ", ?"
        values += (data.get('order_index'),)
    
    if data.get('parent_task_id'):
        columns += ", parent_task_id"
        placeholders += ", ?"
        values += (data.get('parent_task_id'),)

    query = f"""
        INSERT INTO tasks ({columns})
        VALUES ({placeholders})
    """
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    dbCur.execute(query, values)
    dbCon.commit()
    dbCon.close()
    
    if data.get('parent_task_id'):
        add_subtask()

    return redirect(url_for('index'))

@app.route("/update", methods=['POST'])
def update_task():
    data = request.get_json()
    query = "UPDATE tasks SET "

    if data.get('task_id'):
        taskId = data.get('task_id')
    
    if data.get('task_title'):
        query += f"task_title = {data.get('task_title')}, "

    if data.get('task_description'):
        query += f"task_description = {data.get('task_description')}, "
    
    if data.get('order_index'):
        query += f"priority = {data.get('order_index')}, "

    if data.get('status'):
        query += f"status = {data.get('status')}, "
    
    if data.get('parent_task_id'):
        query += f"parent_task_id = {data.get('parent_task_id')}, "

    query = query[:-2] + f"WHERE task_id = {taskId}"
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    dbCur.execute(query)
    dbCon.commit()
    dbCon.close()
    return redirect(url_for('index'))

@app.route("/remove/<task_id>")
def remove_task(task_id):
    query = f"DELETE FROM tasks WHERE task_id={task_id}"
    dbCon = make_db_connection()
    dbCur = dbCon.cursor()
    dbCur.execute(query)
    dbCon.commit()
    dbCon.close()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)