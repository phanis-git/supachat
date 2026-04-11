

// working 2
import React, { useState } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip
} from "recharts";

function App() {
  const [query, setQuery] = useState("");
  const [data, setData] = useState([]);

  const sendQuery = async () => {
    try {
      const res = await axios.post("/api/query", {
        query: query
      });
      // ✅ Check if response has error
    if (res.data.error) {
      alert("DB Error: " + res.data.error);
      return;
    }

    if (res.data.data) {
      setData(res.data.data);
    } else {
      setData([]);
    }
    } catch (err) {
      alert("Error fetching data");
    }
  };

  return (
    <div className="container">
<div style={{ padding: "20px" }}>
      <h2>SupaChat</h2>

      <div className="input-group">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something..."
      />
      <button onClick={sendQuery}>Send</button>
      </div>

      <h3>Results</h3>

      <table border="1">
        <thead>
          <tr>
            {data[0] &&
              Object.keys(data[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              {Object.values(row).map((val, j) => (
                <td key={j}>{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <BarChart width={400} height={300} data={data}>
        <XAxis dataKey="topic" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="views" />
      </BarChart>
    </div>
    </div>
  );
}

export default App;