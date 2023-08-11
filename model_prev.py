import yfinance as yf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score

# create data set
def create_dataset(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size])
    return np.array(X), np.array(y)

def create_prediction_model(ticker):
    # Step 1: Gather historical stock price data
    data = yf.download(ticker, period='1y')['Close']
    print(data)

    # Step 2: Prepare the data (reuse the create_dataset function from the previous example)
    window_size = 60
    X, y = create_dataset(data, window_size)
    print(X)

    # Step 3: Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 4: Create and train the SVR model
    model = SVR(kernel='rbf', C=100, epsilon=0.1)  # You can try different kernel functions and hyperparameters
    model.fit(X_train, y_train)
    confidence = model.score(X_test, y_test)
    print(confidence)

    # Step 5: Make predictions
    y_pred = model.predict(X_test)

        # # Step 6: Evaluate the model
        # mse = mean_squared_error(y_test, y_pred)
        # rmse = np.sqrt(mse)
        # r2 = r2_score(y_test, y_pred)

        # print(f'Mean Squared Error (MSE): {mse}')
        # print(f'Root Mean Squared Error (RMSE): {rmse}')
        # print(f'R-squared (R2): {r2}')

    return model

# # Step 6: Evaluate the model
# mse = mean_squared_error(y_test, y_pred)
# rmse = np.sqrt(mse)
# r2 = r2_score(y_test, y_pred)

# print(f'Mean Squared Error (MSE): {mse}')
# print(f'Root Mean Squared Error (RMSE): {rmse}')
# print(f'R-squared (R2): {r2}')

create_prediction_model('AAPL')