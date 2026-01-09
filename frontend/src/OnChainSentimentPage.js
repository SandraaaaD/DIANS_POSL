import React from "react";
import { useParams } from "react-router-dom";
import OnChainSentiment from "./OnChainSentiment";

const OnChainSentimentPage = () => {
    const { symbol } = useParams();

    return (
        <div style={{ padding: "20px" }}>
            <OnChainSentiment initialSymbol={symbol || "BTCUSDT"} />
        </div>
    );
};

export default OnChainSentimentPage;
