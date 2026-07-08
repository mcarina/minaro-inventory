# Minaro-inventory
Controle de estoque de produtos de t.i

## Tecnologias

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT Authentication
- Pydantic
- Docker
- Pytest

## Funcionalidades

- Autenticação com JWT
- Controle de usuários
- Controle de permissões (RBAC)
- Cadastro de produtos
- Categorias
- Marcas
- Fornecedores
- Controle de estoque
- Movimentação de entrada e saída
- Gestão de patrimônio
- Empréstimos de equipamentos
- Documentação automática da API (Swagger)

## Fluxo

```
Cliente
      │
      ▼
 FastAPI
      │
      ▼
 Service Layer
      │
      ▼
 Repository
      │
      ▼
 PostgreSQL
```


## Como executar

```
docker compose up -d
```

## Swagger

```
http://localhost:8000/docs
```

## Fluxo das tabelas no banco
<img width="921" height="1111" alt="inventory drawio" src="https://github.com/user-attachments/assets/d3a9afb3-b16b-4106-9241-492669503ab1" />

