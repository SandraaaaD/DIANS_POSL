import numpy as np
from sklearn.preprocessing import MinMaxScaler

def prepare_lstm_data(df, lookback=30):
    prices = df[['close']].values

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(prices)

    X, y = [], []

    for i in range(lookback, len(scaled)):
        X.append(scaled[i-lookback:i, 0])
        y.append(scaled[i, 0])

    X = np.array(X)
    y = np.array(y)

    X = X.reshape((X.shape[0], X.shape[1], 1))

    return X, y, scaler
