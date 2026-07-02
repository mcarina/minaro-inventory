from fastapi import FastAPI
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.roles.router import router as roles_router

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(roles_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
