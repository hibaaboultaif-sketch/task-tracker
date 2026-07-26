from fastapi import FastAPI, HTTPException

from app.models import Status, TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()

tasks: dict[int, TaskResponse] = {}
next_task_id = 1

VALID_STATUS_TRANSITIONS = {
    Status.ToDo: {Status.ToDo, Status.InProgress},
    Status.InProgress: {Status.InProgress, Status.Done},
    Status.Done: {Status.Done},
}


def validate_status_transition(current: Status, new: Status) -> None:
    if new not in VALID_STATUS_TRANSITIONS[current]:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid status transition from '{current.value}' to '{new.value}'. "
                "Status can only move forward: ToDo -> InProgress -> Done."
            ),
        )


@app.get("/")
def root():
    return {"message": "Task Tracker API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_create: TaskCreate):
    global next_task_id
    task = TaskResponse(id=next_task_id, **task_create.model_dump())
    tasks[next_task_id] = task
    next_task_id += 1
    return task


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(status: Status | None = None):
    result = list(tasks.values())
    if status is not None:
        result = [task for task in result if task.status == status]
    return result


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = task_update.model_dump(exclude_unset=True)
    if not updates:
        return tasks[task_id]

    current = tasks[task_id]
    if "status" in updates:
        validate_status_transition(current.status, updates["status"])

    updated = current.model_copy(update=updates)
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
