from fastapi import FastAPI
import sqlite3
from Routers.route import router as task_router

app = FastAPI(title="Task Management API",description="Api to manage tasks")

@app.get("/")
def home():
    return{
        "message":"Hello , Welcome to Task Management API"
    }

app.include_router(task_router) 