import numpy as np
from sklearn.preprocessing import MinMaxScaler
from lstm_model import build_lstm


def train_lstm(df, lookback=30):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[["close"]])

    X, y = [], []
    for i in range(lookback, len(scaled)):
        X.append(scaled[i - lookback:i])
        y.append(scaled[i])

    X, y = np.array(X), np.array(y)

    split = int(0.7 * len(X))
    X_train, y_train = X[:split], y[:split]

    model = build_lstm((lookback, 1))
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    last_window = X[-1].reshape((1, lookback, 1))

    scaled_pred = model.predict(last_window)[0][0]
    predicted_price = scaler.inverse_transform([[scaled_pred]])[0][0]

    last_price = df["close"].values[-1]

    change_percent = (predicted_price - last_price) / last_price


    prob_up = 1 / (1 + np.exp(-change_percent * 20))  
    prob_down = 1 - prob_up

    prob_up = max(0.01, min(0.99, prob_up))
    prob_down = max(0.01, min(0.99, prob_down))

    print(f"   LSTM Results:")
    print(f"   Last price: {last_price:.2f}")
    print(f"   Predicted price: {predicted_price:.2f}")
    print(f"   Change: {change_percent * 100:.2f}%")
    print(f"   Prob up: {prob_up:.4f} ({prob_up * 100:.1f}%)")
    print(f"   Prob down: {prob_down:.4f} ({prob_down * 100:.1f}%)")

    last_window = X[-1].reshape((1, lookback, 1))
    scaled_pred = model.predict(last_window)[0][0]
    predicted_price = scaler.inverse_transform([[scaled_pred]])[0][0]

    last_close = df['close'].iloc[-1]
    change_percent = (predicted_price - last_close) / last_close
    prob_up = max(0.01, min(0.99, 1 / (1 + np.exp(-change_percent * 20))))
    prob_down = 1 - prob_up

    return model, scaler, last_window, predicted_price, prob_up, prob_down

