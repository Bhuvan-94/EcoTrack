import os
import pandas as pd
import random
import pickle
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

MODEL_FILE = "model.pkl"
DATA_FILE = "carbon_data.csv"

def generate_dataset(n=500):
    records = []
    for _ in range(n):
        distance = round(random.uniform(1, 50), 2)
        electricity = round(random.uniform(1, 20), 2)
        shopping = random.randint(0, 10)

        mode = random.choice(["car", "bike", "bus", "walk"])
        food = random.choice(["veg", "non-veg"])

        mode_factor = {"car": 2.5, "bike": 0.5, "bus": 1.2, "walk": 0}
        food_factor = {"veg": 1.5, "non-veg": 3.0}

        co2 = (
            distance * mode_factor[mode] +
            electricity * 0.8 +
            food_factor[food] +
            shopping * 0.3
        )

        records.append([distance, mode, electricity, food, shopping, round(co2, 2)])

    df = pd.DataFrame(records, columns=[
        "distance", "mode", "electricity", "food", "shopping", "co2"
    ])

    df.to_csv(DATA_FILE, index=False)

def preprocess(data):
    mode_map = {"car": 3, "bike": 1, "bus": 2, "walk": 0}
    food_map = {"veg": 0, "non-veg": 1}

    return [
        float(data["distance"]),
        mode_map[data["mode"]],
        float(data["electricity"]),
        food_map[data["food"]],
        int(data["shopping"])
    ]

def train_model():
    if not os.path.exists(DATA_FILE):
        generate_dataset()

    df = pd.read_csv(DATA_FILE)

    df["mode"] = df["mode"].map({"car": 3, "bike": 1, "bus": 2, "walk": 0})
    df["food"] = df["food"].map({"veg": 0, "non-veg": 1})

    X = df.drop("co2", axis=1)
    y = df["co2"]

    model = RandomForestRegressor()
    model.fit(X, y)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

def load_model():
    if not os.path.exists(MODEL_FILE):
        train_model()
    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)

model = load_model()

def suggestion(co2):
    if co2 < 10:
        return "Low emission. Keep it up!"
    elif co2 < 25:
        return "Moderate emission. Try public transport."
    else:
        return "High emission! Reduce car use and electricity."

@app.route("/")
def home():
    return "EcoTrack API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    processed = preprocess(data)
    result = model.predict([processed])[0]

    return jsonify({
        "predicted_co2": round(result, 2),
        "suggestion": suggestion(result)
    })

if __name__ == "__main__":
    app.run(debug=True)
