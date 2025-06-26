# main.py
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Allow frontend tools (Altair, React apps) to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
