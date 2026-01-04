from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from .webui_api import router
import json

app = FastAPI()

@app.get("/")
async def serve_index():
    try:
        with open("serveur/static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend file not found")

app.include_router(router, prefix="/api")

app.mount("/static", StaticFiles(directory="serveur/static", html=True), name="static")

def runapi_server(host = "127.0.0.1",port=8088):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
   