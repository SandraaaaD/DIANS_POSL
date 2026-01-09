import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function Dashboard() {
    const [symbols, setSymbols] = useState([]);
    const [selectedSymbol, setSelectedSymbol] = useState("");
    const [timeframe, setTimeframe] = useState("1d");
    const [days, setDays] = useState(7);

    const [indicatorData, setIndicatorData] = useState(null);
    const [lstmPrediction, setLstmPrediction] = useState(null);

    useEffect(() => {
        const loadSymbols = async () => {
            try {
                const res = await axios.get("http://127.0.0.1:8000/symbols");
                setSymbols(res.data);
                if (res.data.length > 0) setSelectedSymbol(res.data[0]);
            } catch (err) {
                console.error(err);
            }
        };
        loadSymbols();
    }, []);

    useEffect(() => {
        if (!selectedSymbol) return;

        const fetchIndicators = async () => {
            try {
                const res = await axios.get(
                    `http://127.0.0.1:8000/indicators/${selectedSymbol}?timeframe=${timeframe}`
                );
                setIndicatorData(res.data);
            } catch (err) {
                console.error(err);
                setIndicatorData({ indicators: {}, signals: {} });
            }
        };
        fetchIndicators();
    }, [selectedSymbol, timeframe]);

    useEffect(() => {
        if (!selectedSymbol) return;

        const fetchPrediction = async () => {
            try {
                const res = await axios.get(
                    `http://127.0.0.1:8000/lstm/predict?symbol=${selectedSymbol}&days=${days}`
                );
                setLstmPrediction(res.data);
            } catch (err) {
                console.error(err);
                setLstmPrediction(null);
            }
        };
        fetchPrediction();
    }, [selectedSymbol, days]);

    if (!indicatorData || !indicatorData.indicators || Object.keys(indicatorData.indicators).length === 0)
        return <div>Loading indicators...</div>;

    const labels = Object.keys(indicatorData.indicators);
    const ema = labels.map((d) => indicatorData.indicators[d]?.ema ?? null);
    const sma = labels.map((d) => indicatorData.indicators[d]?.sma ?? null);

    const buySignals = labels.map((d, i) =>
        indicatorData.signals[d]?.buy ? ema[i] : null
    );
    const sellSignals = labels.map((d, i) =>
        indicatorData.signals[d]?.sell ? ema[i] : null
    );

    const chartData = {
        labels,
        datasets: [
            { label: "EMA", data: ema, borderColor: "blue", tension: 0.1 },
            { label: "SMA", data: sma, borderColor: "orange", tension: 0.1 },
            { label: "Buy Signal", data: buySignals, pointBackgroundColor: "green", pointRadius: 6, showLine: false },
            { label: "Sell Signal", data: sellSignals, pointBackgroundColor: "red", pointRadius: 6, showLine: false },
        ],
    };

    return (
        <div style={{ width: "95%", margin: "auto", marginTop: "30px", fontFamily: "Arial, sans-serif" }}>
            <h1 style={{ textAlign: "center", marginBottom: "30px" }}>Crypto Dashboard</h1>

            {/* Dropdowns */}
            <div style={{ display: "flex", gap: "20px", marginBottom: "30px", justifyContent: "center", flexWrap: "wrap" }}>
                <div>
                    <label style={{ fontWeight: "bold" }}>Симбол: </label>
                    <select
                        value={selectedSymbol}
                        onChange={(e) => setSelectedSymbol(e.target.value)}
                        style={{ padding: "8px", borderRadius: "6px", border: "1px solid #aaa" }}
                    >
                        <option value="">-- Избери --</option>
                        {symbols.map((s) => (
                            <option key={s} value={s}>{s}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label style={{ fontWeight: "bold" }}>Timeframe: </label>
                    <select
                        value={timeframe}
                        onChange={(e) => setTimeframe(e.target.value)}
                        style={{ padding: "8px", borderRadius: "6px", border: "1px solid #aaa" }}
                    >
                        <option value="1d">1 Day</option>
                        <option value="1w">1 Week</option>
                        <option value="1m">1 Month</option>
                    </select>
                </div>

                <div>
                    <label style={{ fontWeight: "bold" }}>Days : </label>
                    <input
                        type="number"
                        value={days}
                        onChange={(e) => setDays(Number(e.target.value))}
                        style={{ width: "60px", padding: "6px", borderRadius: "6px", border: "1px solid #aaa" }}
                    />
                </div>
            </div>

            {/* Chart */}
            <div className={"chartAndPredict"}>
                <div style={{ marginBottom: "50px" }}>
                    <Line
                        data={chartData}
                        options={{
                            responsive: true,
                            plugins: { legend: { position: "top" }, title: { display: true, text: `${selectedSymbol} ${timeframe} Chart` } },
                        }}
                    />
                </div>

                {/* LSTM Prediction */}
                <div style={{ textAlign: "center", marginBottom: "50px" }}>
                    <h2>LSTM Prediction (Next Price)</h2>
                    {lstmPrediction ? (
                        <>
                            <p>Моментална цена: <b>{ema[ema.length - 1].toFixed(2)}</b></p>
                            <p>Следна цена: <b>{lstmPrediction.predicted_price.toFixed(2)}</b></p>
                            <p>Веројатност за раст: <b>{(lstmPrediction.prob_up * 100).toFixed(1)}%</b></p>
                            <p>Веројатност за пад: <b>{(lstmPrediction.prob_down * 100).toFixed(1)}%</b></p>
                        </>
                    ) : (
                        <p>Loading prediction...</p>
                    )}
                </div>
            </div>
        </div>
    );
}
