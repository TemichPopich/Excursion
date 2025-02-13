from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

from app.users.clients.router import router as client_router
from app.users.guides.router import router as guide_router
from app.users.admins.router import router as admin_router
from app.excursions.router import router as excursion_router

from app.auth.router import router as auth_router

http_bearer = HTTPBearer(auto_error=False)

app = FastAPI(dependencies=[Depends(http_bearer)])


@app.get("/")
def home_page():
    return {"message": "Экскурсии"}


app.include_router(client_router)
app.include_router(guide_router)
app.include_router(admin_router)
app.include_router(excursion_router)
app.include_router(auth_router)
