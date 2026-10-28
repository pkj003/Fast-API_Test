from fastapi import APIRouter,HTTPException,status,Depends
import sqlite3
import operations
from typing import Annotated
from db import get_db
from schemas import ResponseTask,CreateTask,UpdateTask


router = APIRouter(prefix="/task",tags=["TaskManagement"])

Db_connection = Annotated[sqlite3.Connection,Depends(get_db)]

@router.get("/")
def getalltask(conn:Db_connection):
    return operations.displayalltask(conn)

@router.get("/{task_id}",response_model=ResponseTask)
def displaytaskbyid(task_id : int,conn:Db_connection):
    task = operations.gettaskbyid(task_id,conn)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")

    return task

@router.post("/",response_model=ResponseTask,status_code=status.HTTP_201_CREATED)
def createnewtask(conn:Db_connection,task : CreateTask):
    return operations.createtask(task,conn)

@router.put("/{task_id}",response_model=ResponseTask)
def updatenewtask(task_id:int,conn:Db_connection,uptask:UpdateTask):
    update = operations.updatetask(task_id,conn,uptask)
    if update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task Not found")

    return update

@router.delete("/{task_id}")
def delete(conn: Db_connection,task_id : int):
    deleted = operations.deletetask(conn,task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="student not found")
    return deleted
    