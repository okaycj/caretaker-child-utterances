import os
from string import ascii_lowercase as alpha

from flask import Flask, jsonify, render_template, request, session
from werkzeug.wrappers.response import Response

from main import run_prediction

app = Flask(__name__)


if app.debug:
    from dotenv import load_dotenv

    load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def index() -> str:
    """
    Retrieves the utterance from the form and run the model.  This will
    organize the data into three parts (utterance, caretaker percent, and
    child percent) and store them in session.  Session stores the last five
    utterance queries.
    """

    context: dict[str, float | str] = {}
    utterance = request.args.get("utterance")
    utterances = session.get("utterances", [])
    caretaker_percents = session.get("caretaker_percents", [])
    child_percents = session.get("child_percents", [])

    if utterance:
        # Sanitize data
        utterance = " ".join(
            "".join(filter(lambda c: c in alpha, w)) for w in utterance.lower().split()
        )
        context["utterance"] = utterance

        if not utterances or utterances[-1] != utterance:
            prediction = run_prediction(utterance)
            utterances.append(utterance)
            caretaker_percents.append(prediction["caretaker_percent"])
            child_percents.append(prediction["child_percent"])

    session.update(
        utterances=utterances[-5:],
        caretaker_percents=caretaker_percents[-5:],
        child_percents=child_percents[-5:],
    )

    return render_template("index.html", **context)


@app.route("/utterances")
def utterances() -> Response:
    """
    Async call to retrieve session data to populate chart.
    """
    return jsonify(
        {
            "utterances": session["utterances"],
            "caretaker_percents": session["caretaker_percents"],
            "child_percents": session["child_percents"],
        }
    )
