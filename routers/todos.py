from fastapi import (
    APIRouter,
    Path,
    HTTPException,
    status
)
from schemas import TodoRequest
from database import (
    SessionLocal,
    get_db,
    db_dependency
)
from models import Todos

router = APIRouter(prefix="/todo", tags=["Todos"])


@router.get("/all/", status_code=status.HTTP_200_OK)
async def read_all_todos(db: db_dependency):
    return db.query(Todos).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_single_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter_by(id=todo_id).first()
    if todo_model:
        return todo_model
    raise HTTPException(
        status_code=404, detail="Todo NOT found"
    )


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_single_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_single_todo(db: db_dependency, todo_id: int, todo_request: TodoRequest):
    todo_model = db.query(Todos).filter_by(id=todo_id).first()

    if not todo_model:
        raise HTTPException(
            status_code=404, detail="Todo NOT Found")

    todo_model.priority = todo_request.priority
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.complete = todo_request.complete

    db.commit()
# delete request method


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter_by(id=todo_id).first()
    if not todo_model:
        raise HTTPException(
            status_code=404,
            detail="Todo NOT Found"
        )
    db.delete(todo_model)
    db.commit()
