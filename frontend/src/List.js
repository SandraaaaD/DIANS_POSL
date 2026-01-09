import React, { useEffect, useState } from "react";

const List = () => {
    const [state, setState] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [page, setPage] = useState(0);
    const pageSize = 1000;

    useEffect(() => {
        fetch("http://localhost:8080/api/all")
            .then(response => {
                if (!response.ok) throw new Error("Network response was not ok");
                return response.json();
            })
            .then(data => {
                setState(data);
            })
            .catch(err => setError(err.message || "Error при преземање на податоци"))
            .finally(() => setLoading(false));
    }, []);

    const start = page * pageSize;
    const end = start + pageSize;
    const visible = state.slice(start, end);

    const totalPages = Math.ceil(state.length / pageSize);

    return (
      <div className="App" style={{ padding: 20 }}>
        <h1 className={"site_podatoci"}>Сите податоци</h1>

        {loading && <p>Вчитување...</p>}
        {error && <p style={{ color: 'red' }}>Грешка: {error}</p>}

        {!loading && !error && (
            <>
              <p className={"site_podatoci"}>Вкупно записи: {state.length}</p>

              <div className={"site_podatoci"} style={{ marginBottom: 12 }}>
                <button
                    onClick={() => setPage(p => Math.max(0, p - 1))}
                    disabled={page === 0}
                >
                  Претходна
                </button>

                <span style={{ margin: '0 10px' }}>
              Страница {page + 1} од {totalPages || 1}
            </span>

                <button
                    onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
                    disabled={page >= totalPages - 1}
                >
                  Следна
                </button>
              </div>

                <div className={"kopcinja"}>

                </div>

              <div className={"podatoci"}>
                {visible.length === 0 && <p>Нема податоци за прикажување.</p>}

                {visible.map(obj => (
                    <div key={obj.id} style={{
                        padding: 8,
                        borderBottom: '1px solid #ddd'
                    }}>
                        <div className={"podatoci_p"}>
                            <div><strong>ИД:</strong> {obj.id}</div>
                            <div><strong>Симбол:</strong> {obj.symbol}</div>
                            <div><strong>Дата:</strong> {obj.date}</div>
                            <div><strong>Највисока цена:</strong> {obj.high}</div>
                            <div><strong>Најниска цена:</strong> {obj.low}</div>
                            <div><strong>Просечна цена:</strong> {obj.lastPrice}</div>
                            <div><strong>Број на трејдови:</strong> {obj.count}</div>
                        </div>
                    </div>
                ))}
              </div>

              <div className={"site_podatoci"} style={{ marginTop: 12 }}>
                <label>
                  Оди на страница:{' '}
                  <input
                      type="number"
                      min={1}
                      max={totalPages || 1}
                      value={page + 1}
                      onChange={e => {
                        let v = Number(e.target.value || 1);
                        v = Math.max(1, Math.min(totalPages || 1, v));
                        setPage(v - 1);
                      }}
                      style={{ width: 80 }}
                  />
                </label>
              </div>
            </>
        )}
      </div>
  );
};

export default List;
