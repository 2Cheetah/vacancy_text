# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from parser import parser
from groq_client.groq_client import GroqClient
import os
from groq import Groq

app = FastAPI()

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_TOKEN"),
)

templates = Jinja2Templates(directory="templates")

class InputText(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
async def process_text(input_text: InputText):
    md_text = parser.parse_text(groq_client, input_text.text)
    return {"markdown": md_text}
