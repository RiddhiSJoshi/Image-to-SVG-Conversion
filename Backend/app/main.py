# main.py
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Serve static files (JS, CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML at /
@app.get("/")
async def read_index():
    return FileResponse("index.html")

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Allow frontend tools (Altair, React apps) to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
