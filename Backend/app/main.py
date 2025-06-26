# main.py
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from schema import schema
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional: enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount GraphQL API at /graphql
app.add_route("/graphql", GraphQLApp(schema=schema))
