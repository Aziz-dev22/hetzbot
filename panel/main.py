from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from bot.db import get_session, User, Server
import os

app = FastAPI()
templates = Jinja2Templates(directory="panel/templates")
app.mount("/static", StaticFiles(directory="panel/static"), name="static")

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

def verify_admin(request: Request):
    token = request.headers.get("Authorization")
    if token != ADMIN_TOKEN:
        return False
    return True

@app.get("/")
async def dashboard(request: Request, is_admin: bool = Depends(verify_admin)):
    session = get_session()
    users_count = session.query(User).count()
    servers_count = session.query(Server).count()
    servers = session.query(Server).all()
    session.close()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "users_count": users_count,
        "servers_count": servers_count,
        "servers": servers
    })

@app.post("/server/{server_id}/reboot")
async def reboot_server_panel(server_id: int, is_admin: bool = Depends(verify_admin)):
    from bot.hcloud import reboot_server
    success = reboot_server(server_id)
    return {"status": "ok" if success else "error"}
