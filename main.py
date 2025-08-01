from pathlib import Path
from string import punctuation
from typing import Dict, Generator, Optional

import joblib  # type: ignore
import pandas as pd
import pylangacq  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def normalize_role(role: str) -> Optional[str]:
    """
    Take in role from chat file and normalize it to either caretaker or child.
    Ignore roles that could be the investigator.
    """
    if role in {"Mother", "Father", "Adult", "Relative"}:
        return "caretaker"
    if role in {"Target_Child", "Child"}:
        return "child"
    if role in {"Investigator", "Unidentified"}:
        return None
    raise Exception(f"Unknown role: {role}.")


def role_mapping(q: pylangacq.Reader) -> Dict[str, Optional[str]]:
    """
    Generate a dictionary to map the roles in the chat file to the normalized
    roles.
    """
    role_dict = {}

    for header in q.headers():
        for key, value in header["Participants"].items():
            role = normalize_role(value["role"])

            if role in role_dict:
                raise Exception(f"Role already in role dictionary: {role}")
            else:
                role_dict[key] = normalize_role(value["role"])

    return role_dict


def train(d: Generator[tuple[str, str], None, None]) -> None:
    """
    Train regression on CHILDES data and save modal and vectorizer to joblib
    file.
    """
    df = pd.DataFrame(d, columns=["speaker", "utterance"])

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["utterance"])
    y = df["speaker"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "childes.joblib")
    joblib.dump(vectorizer, "vectorizer.joblib")


def preprocess_stoopsmontag() -> Generator[tuple[str, str], None, None]:
    """
    This is the preprocessing for the stoopmontag data. It will filter out
    ending punctuation and normalize role.
    """
    data_dir = str(Path("data/StoopsMontag").absolute())
    q = pylangacq.read_chat(data_dir)
    role_dict = role_mapping(q)

    for utterance in q.utterances():
        token_words = (t.word for t in utterance.tokens)
        words = filter(lambda w: w not in punctuation, token_words)
        sentence = " ".join(words)
        role = role_dict[utterance.participant]

        if sentence and role:
            yield role, sentence


def run_prediction(value: str) -> dict[str, float | str]:
    """
    Function used by view to get prediction of single utterance.
    """
    loaded_model = joblib.load("childes.joblib")
    loaded_vectorizer = joblib.load("vectorizer.joblib")
    new_data_point_vectorized = loaded_vectorizer.transform([value])
    # This is a list of probabilities, the prediction informs the order of
    # values.  Here we're assuming caretaker is the 0 index and the child is the
    # other.
    proba = loaded_model.predict_proba(new_data_point_vectorized)
    predict = loaded_model.predict(new_data_point_vectorized)
    return {
        "caretaker_percent": float(proba[0][0]),
        "child_percent": float(proba[0][1]),
        "prediction": str(predict[0]),
    }


if __name__ == "__main__":
    train(preprocess_stoopsmontag())
