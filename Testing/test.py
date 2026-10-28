import sqlite3

import pytest
from fastapi.testclient import TestClient

from db import get_db
from main import app


@pytest.fixture
def client():
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL CHECK(length(Title) > 0),
            Description TEXT NOT NULL DEFAULT '',
            Priority TEXT NOT NULL CHECK(Priority IN ('low', 'medium', 'high')),
            Taskstatus TEXT NOT NULL CHECK(
                Taskstatus IN ('pending', 'in progress', 'completed')
            )
        )
        """
    )
    connection.commit()

    def override_get_db():
        yield connection

    original_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        if original_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = original_override
        connection.close()


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello , Welcome to Task Management API"
    }


def test_get_all_tasks(client):
    response = client.get("/task/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_task(client):
    payload = {
        "Title": "Write tests",
        "Description": "Cover the task API",
        "Priority": "high",
        "Taskstatus": "pending",
    }

    create_response = client.post("/task/", json=payload)

    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task == {"id": 1, **payload}

    get_response = client.get("/task/1")

    assert get_response.status_code == 200
    assert get_response.json() == created_task


def test_get_task_not_found(client):
    response = client.get("/task/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client):
    create_response = client.post(
        "/task/",
        json={
            "Title": "Old title",
            "Description": "Old description",
            "Priority": "low",
            "Taskstatus": "pending",
        },
    )
    assert create_response.status_code == 201

    update_payload = {
        "Title": "Updated title",
        "Description": "Updated description",
        "Priority": "medium",
        "Taskstatus": "in progress",
    }
    response = client.put("/task/1", json=update_payload)

    assert response.status_code == 200
    assert response.json() == {"id": 1, **update_payload}


def test_update_task_not_found(client):
    response = client.put(
        "/task/999",
        json={
            "Title": "Missing task",
            "Description": "",
            "Priority": "medium",
            "Taskstatus": "pending",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task Not found"


def test_delete_task(client):
    create_response = client.post(
        "/task/",
        json={
            "Title": "Delete me",
            "Description": "",
            "Priority": "medium",
            "Taskstatus": "pending",
        },
    )
    assert create_response.status_code == 201

    response = client.delete("/task/1")

    assert response.status_code == 200
    assert response.json() == {"message": "deleted succesfully", "id": 1}
    assert client.get("/task/1").status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/task/999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {
            "Title": "",
            "Description": "",
            "Priority": "medium",
            "Taskstatus": "pending",
        },
        {
            "Title": "Invalid priority",
            "Description": "",
            "Priority": "urgent",
            "Taskstatus": "pending",
        },
        {
            "Title": "Invalid status",
            "Description": "",
            "Priority": "low",
            "Taskstatus": "started",
        },
    ],
)
def test_create_task_rejects_invalid_payload(client, payload):
    response = client.post("/task/", json=payload)

    assert response.status_code == 422