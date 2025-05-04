from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TEMPORARY fix, use wildcard for now to debug
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoItem(BaseModel):
    id: int
    content: str

class TodoItemCreate(BaseModel):
    content: str

todos: List[TodoItem] = []
id_counter = 1

@app.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    global id_counter
    new_todo = TodoItem(id=id_counter, content=item.content)
    todos.append(new_todo)
    id_counter += 1
    return new_todo

@app.get("/todos", response_model=List[TodoItem])
async def read_todos():
    return todos

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
