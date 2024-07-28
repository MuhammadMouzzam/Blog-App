from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blogs, users, auth, comments, votes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Twitter (Clone)',summary='This is my 1st ever project using FastApi', description="Here, you can post Blogs, add comments, and also like any blog if you find it interesting. This is a CRUD based application meaning you can create, delete, update and read blogs.")


@app.get("/")
def main_page():
    return "Welcome to my Blogs Site"


app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(votes.router)




