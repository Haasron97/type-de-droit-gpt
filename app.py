from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/identifier", methods=["POST"])
def identifier():
    data = request.get_json()
    texte = data.get("texte", "")
    prompt = f"Indique uniquement le type de droit concerné (exemple : Droit du travail, Droit pénal, Droit civil, etc.) pour le cas suivant :\n\n{texte}\n\nRéponds seulement par le type de droit."
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.5
        )
        reponse = completion.choices[0].message["content"].strip()
        return jsonify({"type": reponse})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)