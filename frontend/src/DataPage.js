import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

function DataPage() {
    const { symbol } = useParams();
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8080/api/symbol/${symbol}`)
            .then(res => res.json())
            .then(json => setData(json))
            .catch(err => console.error(err));
    }, [symbol]);

    const chartData = data.map(item => ({
        date: item.date,
        close: item.close
    }));

    const latest = data.length > 0 ? data[data.length - 1] : null;

    return (
        <div className="symbol">
            <h1>Податоци за: {symbol}</h1>

            {latest ? (
                <div className="latest-data">
                    <h2>Најнови податоци</h2>
                    <p>Симбол: {latest.symbol}</p>
                    <p>Последна цена: {latest.close}</p>
                    <p>Отворање: {latest.open}</p>
                </div>
            ) : (
                <p>Вчитување....</p>
            )}

            {data.length > 0 && (
                <>
                    <h2 className={"centar"}>Дијаграм на цените</h2>
                    <ResponsiveContainer width="100%" height={400}>
                        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="date" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="close" stroke="#8884d8" activeDot={{ r: 8 }} />
                        </LineChart>
                    </ResponsiveContainer>
                </>
            )}
        </div>
    );
}

export default DataPage;
