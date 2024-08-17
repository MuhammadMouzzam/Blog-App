from fastapi import FastAPI
from . import models
from .database import engine
from starlette.middleware.sessions import SessionMiddleware
from .routers import blogs, users, auth, comments, votes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Blogs App', description="This is my 1st ever project using FastApi. Here, you can post Blogs, add comments, and also like any blog if you find it interesting. This is a CRUD based application meaning you can create, delete, update and read blogs.")
app.add_middleware(SessionMiddleware, secret_key='this_is_just_a_random_key')

# app.add_middleware(SessionMiddleware, secret_key='HHEHEHEHEHE')

@app.get("/")
def main_page():
    return "Welcome to my Blogs Site"


app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(votes.router)




