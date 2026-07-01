import sys
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

sys.path.insert(0, str(Path(__file__).parent))
from modules import memory, scripts, ollama, updater

app = FastAPI(title="OpenCode Ultimate Panel")

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


async def get_context(request: Request):
    user = memory.get_active_user()
    user_files = memory.get_user_files(user)
    users_list = memory.get_users()
    all_models = ollama.list_models_sync()
    ollama_status = await ollama.is_ollama_running()
    update_info = await updater.check_update()
    script_list = scripts.list_scripts()
    sessions = memory.get_sessions(user)
    return {
        "request": request,
        "user": user,
        "users": users_list,
        "user_files": user_files,
        "models": all_models,
        "ollama_ok": ollama_status,
        "update": update_info,
        "scripts": script_list,
        "sessions": sessions,
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    ctx = await get_context(request)
    ctx["page"] = "dashboard"
    return templates.TemplateResponse("dashboard.html", ctx)


@app.post("/switch-user")
async def switch_user(request: Request, username: str = Form(...)):
    memory.set_active_user(username)
    return RedirectResponse("/", status_code=303)


@app.post("/save-memory")
async def save_memory(request: Request, filename: str = Form(...), content: str = Form(...)):
    user = memory.get_active_user()
    memory.save_user_file(user, filename, content)
    return RedirectResponse("/", status_code=303)


@app.post("/run-script")
async def run_script(request: Request, script_name: str = Form(...)):
    result = scripts.run_script(script_name)
    ctx = await get_context(request)
    ctx["page"] = "dashboard"
    ctx["script_result"] = result
    return templates.TemplateResponse("dashboard.html", ctx)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
