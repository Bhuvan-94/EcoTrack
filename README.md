# EcoTrack - Carbon Footprint Predictor

## Overview
EcoTrack is a machine learning-based web API that predicts carbon emissions based on daily activities.

## Features
- Predict CO2 emission
- Suggest eco-friendly actions
- Auto dataset generation
- ML model training included

## Tech Stack
- Python
- Flask
- Scikit-learn

## Setup Instructions

1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   python app.py

3. Open browser:
   http://127.0.0.1:5000/

## API Usage

POST /predict

Example Input:
{
  "distance": 10,
  "mode": "car",
  "electricity": 5,
  "food": "veg",
  "shopping": 2
}

Output:
{
  "predicted_co2": 18.5,
  "suggestion": "Moderate emission. Try public transport."
}

## Project Highlights
- Uses Random Forest Regression
- Fully automated pipeline
- Clean and simple implementation

## Future Scope
- Mobile app integration
- Real-time tracking
