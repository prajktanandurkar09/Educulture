import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".env"))

print("API KEY FROM ENV =", os.getenv("GROQ_API_KEY"))


app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key="GROQ_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-story", methods=["POST"])
def generate_story():
    data = request.get_json()
    topic = data.get("topic", "")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a cultural storyteller."},
            {"role": "user", "content": f"Explain {topic} in simple words."}
        ]
    )

    return jsonify({
        "story": response.choices[0].message.content
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

