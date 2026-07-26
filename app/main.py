from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import Status, TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def compute_is_overdue(task: TaskResponse) -> bool:
    if task.due_date is None:
        return False
    if task.status == Status.Done:
        return False
    try:
        due = date.fromisoformat(task.due_date)
    except ValueError:
        return False
    return due < date.today()


def with_overdue_flag(task: TaskResponse) -> TaskResponse:
    return task.model_copy(update={"is_overdue": compute_is_overdue(task)})


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
    return with_overdue_flag(task)


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    status: Status | None = None,
    tag: str | None = None,
    overdue: bool | None = None,
):
    result = [with_overdue_flag(task) for task in tasks.values()]

    if status is not None:
        result = [task for task in result if task.status == status]

    if tag is not None:
        result = [task for task in result if tag in task.tags]

    if overdue is True:
        result = [task for task in result if task.is_overdue]

    return result


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return with_overdue_flag(tasks[task_id])


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = task_update.model_dump(exclude_unset=True)
    if not updates:
        return with_overdue_flag(tasks[task_id])

    current = tasks[task_id]
    if "status" in updates:
        validate_status_transition(current.status, updates["status"])

    updated = current.model_copy(update=updates)
    tasks[task_id] = updated
    return with_overdue_flag(updated)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]