from fastapi import FastAPI
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.roles.router import router as roles_router
from app.categorias.router import router as categorias_router
from app.localizacoes.router import router as localizacoes_router
from app.marcas.router import router as marcas_router
from app.setores.router import router as setores_router
from app.produtos.router import router as produtos_router
from app.estoques.router import router as estoque_router
from app.movimentacoes.router import router as movimentacao_router
from app.patrimonios.router import router as patrimonio_router

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(categorias_router)
app.include_router(localizacoes_router)
app.include_router(marcas_router)
app.include_router(setores_router)
app.include_router(produtos_router)
app.include_router(estoque_router)
app.include_router(movimentacao_router)
app.include_router(patrimonio_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
