import os
from flask import Flask, render_template, request, jsonify
from chatbot import ChatbotAkademik

app = Flask(__name__)
chatbot = ChatbotAkademik()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Pesan tidak ditemukan"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400

    response = chatbot.get_response(user_message)
    return jsonify({"response": response})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
