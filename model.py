import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import yfinance as yf

def create_prediction_model(stockTicker, forecast_days):
    # get stock adjusted close
    stockTicker = stockTicker
    ticker = yf.Ticker(stockTicker)
    inf = ticker.info
    df = yf.download(inf['symbol'])
    df = df[['Adj Close']]

    # number of days to forecast out
    forecast_out = forecast_days
    df['Prediction'] = df["Adj Close"].shift(-forecast_out)

    # create independent data set
    dfX = df.dropna()
    X = np.array(dfX.drop(labels='Prediction', axis=1))

    # create dependent data set
    dfy = df.dropna()
    y = np.array(dfy['Prediction'])

    # create and train lr model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # test model
    lr_confidence = lr.score(X_test, y_test)
    print(f"LR Confidence: {lr_confidence}")

    # construct prediction data frame
    x_forecast = np.array(df.drop(labels='Prediction', axis=1))[-forecast_out:]
    print(x_forecast)
    lr_prediction = lr.predict(x_forecast)
    print(lr_prediction)


    date_array = generate_date_array(datetime.now().date(), forecast_days)
    forecast_data = {
        'Date': date_array,
        'Forecast': list(lr_prediction)
        }

    return forecast_data

def generate_date_array(start_date, num_days):
    date_array = []
    current_date = start_date
    for _ in range(num_days):
        date_array.append(current_date)
        current_date += timedelta(days=1)
    return date_array

if __name__ == "__main__":
    prediction = create_prediction_model('aapl', 30)
    forecast_data = {
        'Date': [i for i in range(30)],
        'Forecast': list(prediction)
        }