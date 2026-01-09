import React, { useState } from "react";

function OnChainSentiment({ initialSymbol = "BTCUSDT" }) {
    const [symbol, setSymbol] = useState(initialSymbol);
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFetch = async () => {
        setLoading(true);
        setError("");
        setData(null);

        try {
            const response = await fetch(
                `http://localhost:8000/onchain-sentiment/${symbol}`
            );

            const result = await response.json();

            if (result.error) {
                setError(result.error);
            } else {
                setData(result);
            }
        } catch (err) {
            setError("Error fetching data from backend");
        }

        setLoading(false);
    };

    return (
        <div className="onchain-container">
            <h2>On-Chain & Sentiment Analysis</h2>

            <div style={{ marginBottom: "10px" }}>
                <input
                    type="text"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                    placeholder="Enter symbol (e.g. BTCUSDT)"
                />
                <button onClick={handleFetch} style={{ marginLeft: "10px" }}>
                    Fetch
                </button>
            </div>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {data && (
                <div style={{ marginTop: "20px" }}>
                    <h3>Symbol: {symbol}</h3>

                    <h4>On-Chain Signal</h4>
                    <p>{data.onchain_signal ?? "N/A"}</p>

                    <h4>Sentiment Signal</h4>
                    <p>{data.sentiment_signal ?? "N/A"}</p>

                    {data.articles && data.articles.length > 0 && (
                        <>
                            <h4>News Articles</h4>
                            <ul>
                                {data.articles.map((a, i) => (
                                    <li key={i}>{a}</li>
                                ))}
                            </ul>
                        </>
                    )}

                    {data.technical && (
                        <>
                            <h4>Technical Analysis</h4>
                            <pre style={{ background: "#f4f4f4", padding: "10px" }}>
                                {JSON.stringify(data.technical, null, 2)}
                            </pre>
                        </>
                    )}

                    <h3>
                        Final Signal:{" "}
                        <span style={{ fontWeight: "bold" }}>
                            {data.final_signal}
                        </span>
                    </h3>
                </div>
            )}
        </div>
    );
}

export default OnChainSentiment;
