# Task Management API

A simple FastAPI project for managing tasks with SQLite as the local database.

## Features
- Create, read, update, and delete tasks
- FastAPI-based REST API
- SQLite persistence
- Clean modular structure with routers and schemas

## Project Structure
- `main.py` - application entry point
- `Routers/route.py` - API routes for task management
- `db.py` - database connection and initialization
- `operations.py` - database operations logic
- `schemas.py` - request/response models
- `taskdb.db` - SQLite database file generated at runtime

## Prerequisites
- Python 3.9+
- pip

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tests:
   ```bash
   python -m pytest
   ```
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
5. In a separate terminal, launch the Streamlit interface:
   ```bash
   streamlit run streamlit_app.py
   ```
6. Open the API in your browser:
   ```text
   http://127.0.0.1:8000
   ```
   Streamlit opens at `http://localhost:8501`. Keep the FastAPI server running
   while using the interface. Use the sidebar to select a UI for each API
   endpoint and configure the FastAPI base URL if it is running elsewhere.

## API Overview
- `GET /` - welcome message
- `GET /task/` - view all tasks
- `GET /task/{task_id}` - get task by ID
- `POST /task/` - create a task
- `PUT /task/{task_id}` - update a task
- `DELETE /task/{task_id}` - delete a task

## Notes
This project is a basic example and can be expanded with authentication, validation, and frontend integration.
