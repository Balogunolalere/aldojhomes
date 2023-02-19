from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# disable the docs
app = FastAPI(docs_url=None, redoc_url=None)

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

@app.post("/sendmail")
async def contact(request: Request, full_name: str = Form(...), email: EmailStr = Form(...), subject: str = Form(...), message: str = Form(...)):
    sender_email = os.getenv("HOST_EMAIL")
    receiver_email  = os.getenv("HOST_EMAIL")
    smtp_server = 'mail.privateemail.com'
    port = 465
    login = sender_email
    password = os.getenv("HOST_PASSWORD")
    messagex = EmailMessage()
    messagex["Subject"] = "Contact Form"
    messagex["From"] = f"Aldoj Homes and Properties <{sender_email}>"
    messagex["To"] = receiver_email
    content = f"""
    \n
    Full Name: {full_name} \n
    Email: {email} \n
    Subject: {subject} \n
    Message: {message} \n
    """.format(full_name=full_name, email=email, subject=subject, message=message)
    messagex.set_content(content)
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(login, password)
    server.send_message(messagex)
    server.quit()
    resp = RedirectResponse(url="/contact", status_code=status.HTTP_302_FOUND)
    return resp


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

