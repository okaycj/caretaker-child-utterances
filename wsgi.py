from flask import Flask, render_template, request

from main import run_prediction

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    phrase = request.form.get("phrase")
    context = {}

    if phrase:
        context["prediction"] = run_prediction(phrase)

    return render_template("index.html", **context)
