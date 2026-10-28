from db import get_db
from schemas import CreateTask,UpdateTask
import sqlite3


def row_to_dict(row):
    if row is None:
        return None

    data = dict(row)

    if "Id" in data:
        data["id"] = data.pop("Id")

    return data

def displayalltask(conn: sqlite3.Connection):
   rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
   return [row_to_dict(row) for row in rows]

def createtask(task : CreateTask,conn : sqlite3.Connection):
    try:
        crt = conn.execute("""
        INSERT INTO tasks (Title,Description,Priority,Taskstatus)
        VALUES (?,?,?,?)""",(task.Title,task.Description,task.Priority,task.Taskstatus))

        conn.commit()
        task_id = crt.lastrowid
        row = conn.execute("SELECT * FROM tasks WHERE id = ?",(task_id,)).fetchone()
        return row_to_dict(row)
    except sqlite3.Error:
     conn.rollback()
     raise

def gettaskbyid(task_id : int,conn: sqlite3.Connection):
   row = conn.execute("SELECT * FROM tasks WHERE id = ?",(task_id,)).fetchone()

   return row_to_dict(row) 


def updatetask(task_id :int,conn:sqlite3.Connection, uptask:UpdateTask):
   try:
      up = conn.execute("""
UPDATE tasks SET Title = ?,Description = ?,Priority = ?,Taskstatus = ? WHERE id = ?""",(uptask.Title,uptask.Description,uptask.Priority,uptask.Taskstatus,task_id))
      if up.rowcount == 0:
           return None
      conn.commit()
      row = conn.execute("SELECT * FROM tasks WHERE id = ?",(task_id,)).fetchone()

      return row_to_dict(row)
   except sqlite3.Error:
       conn.rollback()
       raise

def deletetask(conn:sqlite3.Connection,task_id:int):
   try:
       dele = conn.execute("DELETE FROM tasks WHERE id = ? ",(task_id,))
       if dele.rowcount == 0:
          return False
       conn.commit()
       return {
          "message":"deleted succesfully",
          "id":task_id
       }
   except sqlite3.Error:
       conn.rollback()
       raise