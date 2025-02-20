from fastapi import (
    FastAPI,

)
from fastapi.responses import RedirectResponse
from database import engine
from models import Base
from routers import auth, todos


app = FastAPI(
    title="TODOS",
    description="You can access Todo API(s) from here",
    version="1.0.0",
    debug=True,
)


@app.get("/", tags=["Home"])
async def root():
    return RedirectResponse(url="/docs", status_code=301)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
