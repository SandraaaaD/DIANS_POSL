import numpy as np

def predict_future(model, scaler, last_window, days):
    preds = []
    window = last_window.copy()

    for _ in range(days):
        p = model.predict(window.reshape(1, window.shape[0], 1), verbose=0)
        preds.append(p[0][0])
        window = np.vstack([window[1:], p])

    preds = scaler.inverse_transform(
        np.array(preds).reshape(-1, 1)
    )

    return preds.flatten().tolist()
