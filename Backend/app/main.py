# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from schema import schema
import uvicorn
from pathlib import Path

app = FastAPI()

# Static files (JS, CSS, images)
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML
@app.get("/")
async def read_index():
    return FileResponse(Path("index.html"))

# GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/saved")
async def view_saved_gallery():
    return FileResponse("saved.html")

# CORS for frontend tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Run the server only when executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
