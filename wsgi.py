from flask import Flask, render_template, request

from main import run_prediction

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    context: dict[str, float | str] = {"title": "Care Taker vs. Child Utterances"}

    if request.method == "POST":
        utterance = request.form.get("utterance")
        if utterance:
            prediction = run_prediction(utterance)
            context.update(
                utterance=utterance,
                care_taker_percent=prediction["care_taker_percent"],
                child_percent=prediction["child_percent"],
            )

    return render_template("index.html", **context)
