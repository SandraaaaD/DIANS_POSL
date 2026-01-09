import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Home";
import List from "./List";
import About from "./About";
import Contact from "./Contact";
import Navbar from "./NavBar";
import DataPage from "./DataPage";
import CryptoChart from './CryptoChart';
import { useParams } from 'react-router-dom';
import OnChainPage  from "./OnChainSentiment";

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/list" element={<List />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/data/:symbol" element={<DataPage />} />
        
                <Route path="/chart/:symbol" element={<CryptoChartWrapper />} />
                <Route path="/analysis/:symbol" element={<OnChainPage />} />
            </Routes>
        </Router>
    );
}

function CryptoChartWrapper() {
    const { symbol } = useParams();
    return <CryptoChart symbol={symbol} timeframe="1d" />;
}

export default App;
