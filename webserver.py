from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    
    data = {
        "title": "Josh's Webpage",
        "items": ["Laptop", "Wireless Mouse", "Keyboard"]
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=data
    )