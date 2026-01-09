import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const
    Home = () => {
    const navigate = useNavigate();

    const [coins, setCoins] = useState([]);
    const [selectedCoin, setSelectedCoin] = useState("");


    useEffect(() => {
        const fetchSymbols = async () => {
            try {
                const res = await fetch("http://localhost:8000/symbols");
                const data = await res.json();
                setCoins(data);
            } catch (err) {
                console.error("Грешка при вчитување на симболи:", err);
            }
        };

        fetchSymbols();
    }, []);

    const handleStart = () => {
        if (selectedCoin) {
            navigate(`/chart/${selectedCoin}`);
        } else {
            alert("Ве молиме изберете коин!");
        }
    };


    return (
        <div className="home-container">
            <div className="hero-section">
                <h1>Добредојде во Крипто Анализа</h1>
                <p>Платформа за паметна анализа на крипто пазарот.</p>

                <div className="dropdown-container">
                    <select
                        value={selectedCoin}
                        onChange={(e) => setSelectedCoin(e.target.value)}
                        className="coin-dropdown"
                    >
                        <option value="">-- Избери коин --</option>
                        {coins.map((coin) => (
                            <option key={coin} value={coin}>
                                {coin}
                            </option>
                        ))}
                    </select>
                    <button className="start-button" onClick={handleStart}>
                        Започни
                    </button>

                </div>

                <button className="go-button" onClick={() => navigate("/list")}>
                    База со историски податоци
                </button>

                <button
                    onClick={() => {
                        navigate(`/analysis/btc`);

                    }}
                    style={{padding: "10px"}}
                >
                    Оди на Анализа
                </button>
            </div>
        </div>
    );
    };

export default Home;
