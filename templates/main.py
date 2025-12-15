import os
from dotenv import load_dotenv
from openai import OpenAI

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory (same as Flask)
templates = Jinja2Templates(directory="templates")


# ---------- ROUTES ----------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/health")
def health():
    return {"status": "ok"}


class FightRequest(BaseModel):
    animal1: str
    animal2: str
    biome: str


@app.post("/fight")
def fight(body: FightRequest):
    prompt = (
        f"In a fight between a {body.animal1} and a {body.animal2} in a {body.biome} biome, "
        f"who would win and why?"
    )

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a knowledgeable zoologist and ecologist."},
            {"role": "user", "content": prompt},
        ],
    )

    return {"outcome": completion.choices[0].message.content}
