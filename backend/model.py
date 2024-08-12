import datetime
import joblib
import pandas as pd
from prophet import Prophet
import os

BASE_DIR = os.getcwd()
TODAY = datetime.date.today()
DATA_PATH = "DailyDelhiClimateTrain.csv"

def train(weather_variable="temperature"):
    data = pd.read_csv(DATA_PATH)
    data.columns = ["date", "temperature", "humidity", "wind_speed", "pressure"]
    df_forecast = data.copy()
    df_forecast["ds"] = df_forecast["date"]
    df_forecast["y"] = df_forecast[weather_variable]
    df_forecast = df_forecast[["ds", "y"]]
    df_forecast
    model = Prophet()
    model.fit(df_forecast)
    joblib.dump(model, os.path.join(BASE_DIR, f"{weather_variable}.joblib"))

def predict(weather_variable="temperature", days=7):
    model_file = os.path.join(BASE_DIR, f"{weather_variable}.joblib")
    model = joblib.load(model_file)
    future = TODAY + datetime.timedelta(days=days)
    dates = pd.date_range(
        start="2017-01-01",
        end=future.strftime("%m/%d/%Y"),
    )
    df = pd.DataFrame({"ds": dates})
    forecast = model.predict(df)
    return forecast.tail(days).to_dict("records")

def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = data["yhat"]
    return output
