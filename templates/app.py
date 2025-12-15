from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__, static_folder=".", static_url_path="")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/fight", methods=["POST"])
def fight():
    body = request.json
    animal1 = body.get("animal1")
    animal2 = body.get("animal2")
    biome   = body.get("biome")

    # Construct prompt for GPT
    prompt = (
      f"In a fight between a {animal1} and a {animal2} in a {biome} biome, "
      f"who would win and why? Provide a concise answer."
    )

    completion = client.chat.completions.create(
      model="gpt-4.1-mini",        # choose the model here
      messages=[
        {"role": "system", "content": "You are a knowledgeable zoologist and ecologist."},
        {"role": "user",   "content": prompt}
      ]
    )

    outcome = completion.choices[0].message.content

    return jsonify({ "outcome": outcome })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
