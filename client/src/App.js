import { useEffect, useState } from "react";
import "./App.css";
import { Link } from "react-router-dom";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("api/weather/TNvozanHzMqjFwuLMA3HxVbkZfKeBp")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);
  return (
    <>
      <WebHeader />
      <main>
        <h1 className="font-bold text-4xl px-3 py-5 m-5 ">Live Weather Data</h1>
        <ul className="m-5">
          {data ? (
            data.map((row) => {
              return (
                <li>
                  <ul className="flex py-5 border-b-4 border-black">
                    <li className="px-3 text-3xl">{row.timsestamp}:</li>
                    <li className="text-2xl py-1">{row.temperature}C</li>
                  </ul>
                </li>
              );
            })
          ) : (
            <p>Loading...</p>
          )}
        </ul>
      </main>
    </>
  );
}

const WebHeader = () => {
  return (
    <>
      <header>
        <nav></nav>
      </header>
    </>
  );
};

export default App;
