import numpy as np
from flask import Flask, request, render_template
import pickle
import warnings

warnings.filterwarnings("ignore", message="X does not have valid feature names")

app = Flask(__name__)
model = pickle.load(open("../ufo-model.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]
    countries = ["Australia", "Canada", "Germany", "UK", "US"]

    return render_template(
        "index.html",
        prediction_text=f"Likely country: {countries[output]}",
    )


if __name__ == "__main__":
    # run the application in a local development server.
    # if degug=True, the server automatically reloads any code changes.
    app.run(debug=True)
