from fastapi import FastAPI
from app.models.users.clients.rounter import router as client_router
from app.models.users.guides.router import router as guide_router
from app.models.users.router import router as user_router


app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Экскурсии"}

app.include_router(client_router)
app.include_router(guide_router)
app.include_router(user_router)