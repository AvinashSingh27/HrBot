import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse("Processing...");
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", null, {
        params: { query },
      });
      const jobId = res.data.job_id;
      pollResult(jobId);
    } catch (error) {
      setResponse("Error: Unable to process your request.");
      setLoading(false);
    }
  };

  const pollResult = async (jobId) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.post("http://127.0.0.1:8000/job-status", null, {
          params: { job_id: jobId },
        });
        if (res.data.result) {
          setResponse(`Result: ${res.data.result}`);
          setLoading(false);
          clearInterval(interval);
        }
      } catch (error) {
        setResponse("Error: Unable to fetch result.");
        setLoading(false);
        clearInterval(interval);
      }
    }, 5000); // Poll every 5 seconds
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Chatbot Portal</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your query:
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ margin: "10px", padding: "5px", width: "300px" }}
          />
        </label>
        <button type="submit" style={{ padding: "5px 10px" }}>
          Submit
        </button>
      </form>
      {loading && <p>{response}</p>}
      {!loading && response && <p>{response}</p>}
    </div>
  );
}

export default App;