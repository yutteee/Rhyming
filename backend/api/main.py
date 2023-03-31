from fastapi import FastAPI

from api.routers import rhyme

app = FastAPI()
app.include_router(rhyme.router)