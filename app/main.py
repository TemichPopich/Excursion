from fastapi import FastAPI
from app.models.users.clients.rounter import router


app = FastAPI()


app.include_router(router)