from py.train import train_lstm
from py.predict import predict_future

async def lstm_service(symbol, history_days, future_days):
    model, scaler, last_window, metrics = await train_lstm(
        symbol,
        history_days
    )

    future = predict_future(model, last_window, scaler, future_days)

    return {
        "symbol": symbol,
        "history_days": history_days,
        "future_days": future_days,
        "metrics": metrics,
        "predictions": future.flatten().tolist()
    }
