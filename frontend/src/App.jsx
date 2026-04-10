// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <section id="center">
//         <div className="hero">
//           <img src={heroImg} className="base" width="170" height="179" alt="" />
//           <img src={reactLogo} className="framework" alt="React logo" />
//           <img src={viteLogo} className="vite" alt="Vite logo" />
//         </div>
//         <div>
//           <h1>Get started</h1>
//           <p>
//             Edit <code>src/App.jsx</code> and save to test <code>HMR</code>
//           </p>
//         </div>
//         <button
//           className="counter"
//           onClick={() => setCount((count) => count + 1)}
//         >
//           Count is {count}
//         </button>
//       </section>

//       <div className="ticks"></div>

//       <section id="next-steps">
//         <div id="docs">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#documentation-icon"></use>
//           </svg>
//           <h2>Documentation</h2>
//           <p>Your questions, answered</p>
//           <ul>
//             <li>
//               <a href="https://vite.dev/" target="_blank">
//                 <img className="logo" src={viteLogo} alt="" />
//                 Explore Vite
//               </a>
//             </li>
//             <li>
//               <a href="https://react.dev/" target="_blank">
//                 <img className="button-icon" src={reactLogo} alt="" />
//                 Learn more
//               </a>
//             </li>
//           </ul>
//         </div>
//         <div id="social">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#social-icon"></use>
//           </svg>
//           <h2>Connect with us</h2>
//           <p>Join the Vite community</p>
//           <ul>
//             <li>
//               <a href="https://github.com/vitejs/vite" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#github-icon"></use>
//                 </svg>
//                 GitHub
//               </a>
//             </li>
//             <li>
//               <a href="https://chat.vite.dev/" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#discord-icon"></use>
//                 </svg>
//                 Discord
//               </a>
//             </li>
//             <li>
//               <a href="https://x.com/vite_js" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#x-icon"></use>
//                 </svg>
//                 X.com
//               </a>
//             </li>
//             <li>
//               <a href="https://bsky.app/profile/vite.dev" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#bluesky-icon"></use>
//                 </svg>
//                 Bluesky
//               </a>
//             </li>
//           </ul>
//         </div>
//       </section>

//       <div className="ticks"></div>
//       <section id="spacer"></section>
//     </>
//   )
// }

// export default App

// working 1

// import React, { useState } from "react";
// import axios from "axios";
// import {
//   BarChart, Bar, XAxis, YAxis, Tooltip
// } from "recharts";

// function App() {
//   const [query, setQuery] = useState("");
//   const [data, setData] = useState([]);

//   const sendQuery = async () => {
//     try {
//       const res = await axios.post("http://localhost:8000/query", {
//         query: query
//       });
//       setData(res.data.data);
//     } catch (err) {
//       alert("Error fetching data");
//     }
//   };

//   return (
//     <div style={{ padding: "20px" }}>
//       <h2>SupaChat</h2>

//       <input
//         value={query}
//         onChange={(e) => setQuery(e.target.value)}
//         placeholder="Ask something..."
//       />
//       <button onClick={sendQuery}>Send</button>

//       <h3>Results</h3>

//       <table border="1">
//         <thead>
//           <tr>
//             {data[0] &&
//               Object.keys(data[0]).map((key) => (
//                 <th key={key}>{key}</th>
//               ))}
//           </tr>
//         </thead>
//         <tbody>
//           {data.map((row, i) => (
//             <tr key={i}>
//               {Object.values(row).map((val, j) => (
//                 <td key={j}>{val}</td>
//               ))}
//             </tr>
//           ))}
//         </tbody>
//       </table>

//       <BarChart width={400} height={300} data={data}>
//         <XAxis dataKey="topic" />
//         <YAxis />
//         <Tooltip />
//         <Bar dataKey="views" />
//       </BarChart>
//     </div>
//   );
// }

// export default App;


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
      const res = await axios.post("http://98.90.200.120:8000/query", {
        query: query
      });
      setData(res.data.data);
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