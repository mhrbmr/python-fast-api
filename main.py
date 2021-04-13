from fastapi import FastAPI

from app import database
import app.routes.auth as auth
import app.routes.blog as blog
import app.routes.users as users


database.Base.metadata.create_all(database.engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(users.router)