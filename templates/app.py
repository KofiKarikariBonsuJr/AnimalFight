import os
from dotenv import load_dotenv
from openai import OpenAI

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

app = FastAPI()

# Serve your static homepage (expects ./index.html in the working directory)
@app.get("/")
def index():
    return FileResponse("index.html")

# Optional: used by your Docker HEALTHCHECK
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

    outcome = completion.choices[0].message.content
    return {"outcome": outcome}
