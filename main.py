from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/services")
async def home(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@app.get("/contact")
async def contacts(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/properties")
async def properties(request: Request):
    return templates.TemplateResponse("properties.html", {"request": request})

# admin panel to add images and video media, it should save and be loaded from a json file
# @app.get("/admin")
# async def admin(request: Request):
#     return templates.TemplateResponse("admin.html", {"request": request})

@app.middleware("http")
async def fix_mime_type(request: Request, call_next):
    response = await call_next(request)
    content_types = {
        ".ttf" :"font/ttf",
        ".woff": "font/woff", 
        ".woff2": "font/woff2"
    }
    for e in content_types:
        if request.url.path.endswith(e): response.headers["Content-Type"] = content_types[e]
    return response

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 200:
        response.headers["Cache-Control"] = "public, max-age=1200"
    return response

