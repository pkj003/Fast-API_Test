import requests
import streamlit as st


st.set_page_config(page_title="Task Manager", page_icon="✅", layout="wide")
st.title("Task Management")
st.caption("Manage tasks through the FastAPI service.")

with st.sidebar:
    st.header("API connection")
    api_url = st.text_input("FastAPI base URL", value="http://127.0.0.1:8000")
    page = st.radio(
        "Choose an endpoint",
        [
            "Home",
            "List tasks",
            "Get task",
            "Create task",
            "Update task",
            "Delete task",
        ],
    )

base_url = api_url.strip().rstrip("/")


def call_api(method: str, path: str, payload: dict | None = None) -> None:
    try:
        response = requests.request(
            method,
            f"{base_url}{path}",
            json=payload,
            timeout=10,
        )
    except requests.RequestException as error:
        st.error(f"Could not reach the FastAPI service: {error}")
        return

    if response.ok:
        st.success(f"Request completed (HTTP {response.status_code}).")
    else:
        st.error(f"Request failed (HTTP {response.status_code}).")

    try:
        st.json(response.json())
    except requests.exceptions.JSONDecodeError:
        st.code(response.text or "(empty response)")


def task_fields(key_prefix: str) -> dict:
    title = st.text_input("Title", max_chars=120, key=f"{key_prefix}_title")
    description = st.text_area(
        "Description", max_chars=2000, key=f"{key_prefix}_description"
    )
    priority = st.selectbox(
        "Priority", ["low", "medium", "high"], key=f"{key_prefix}_priority"
    )
    task_status = st.selectbox(
        "Status",
        ["pending", "in progress", "completed"],
        key=f"{key_prefix}_status",
    )
    return {
        "Title": title,
        "Description": description,
        "Priority": priority,
        "Taskstatus": task_status,
    }


if page == "Home":
    st.subheader("API welcome endpoint")
    st.write("Calls `GET /` on the FastAPI service.")
    if st.button("Check API", type="primary"):
        call_api("GET", "/")

elif page == "List tasks":
    st.subheader("List all tasks")
    st.write("Calls `GET /task/`.")
    if st.button("Load tasks", type="primary"):
        call_api("GET", "/task/")

elif page == "Get task":
    st.subheader("Get a task by ID")
    st.write("Calls `GET /task/{task_id}`.")
    task_id = st.number_input("Task ID", min_value=1, step=1, key="get_task_id")
    if st.button("Get task", type="primary"):
        call_api("GET", f"/task/{task_id}")

elif page == "Create task":
    st.subheader("Create a task")
    st.write("Calls `POST /task/`.")
    with st.form("create_task_form"):
        payload = task_fields("create")
        submitted = st.form_submit_button("Create task", type="primary")
    if submitted:
        if not payload["Title"].strip():
            st.error("Title is required.")
        else:
            call_api("POST", "/task/", payload)

elif page == "Update task":
    st.subheader("Update a task")
    st.write("Calls `PUT /task/{task_id}`.")
    task_id = st.number_input("Task ID", min_value=1, step=1, key="update_task_id")
    with st.form("update_task_form"):
        payload = task_fields("update")
        submitted = st.form_submit_button("Update task", type="primary")
    if submitted:
        if not payload["Title"].strip():
            st.error("Title is required.")
        else:
            call_api("PUT", f"/task/{task_id}", payload)

elif page == "Delete task":
    st.subheader("Delete a task")
    st.write("Calls `DELETE /task/{task_id}`.")
    task_id = st.number_input("Task ID", min_value=1, step=1, key="delete_task_id")
    if st.button("Delete task", type="primary"):
        call_api("DELETE", f"/task/{task_id}")
