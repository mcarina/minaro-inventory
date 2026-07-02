from fastapi import FastAPI
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.roles.router import router as roles_router
from app.categorias.router import router as categorias_router
from app.localizacoes.router import router as localizacoes_router

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(categorias_router)
app.include_router(localizacoes_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
