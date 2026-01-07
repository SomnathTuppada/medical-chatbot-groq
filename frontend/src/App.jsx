import { useState } from "react";
import axios from "axios";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await axios.get("http://127.0.0.1:8000/query", {
        params: { question },
      });

      setAnswer(response.data.answer);
      setSources(response.data.sources);
    } catch (err) {
      setError("Failed to fetch response from backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>🧠 Medical RAG Chatbot</h1>

        <div style={styles.inputRow}>
          <input
            style={styles.input}
            type="text"
            placeholder="Ask a medical question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          />
          <button style={styles.button} onClick={askQuestion}>
            Ask
          </button>
        </div>

        {loading && <p style={styles.loading}>Thinking...</p>}
        {error && <p style={styles.error}>{error}</p>}

        {answer && (
          <div style={styles.answerBox}>
            <h3>Answer</h3>
            <p>{answer}</p>
          </div>
        )}

        {sources.length > 0 && (
          <div style={styles.sourcesBox}>
            <h4>Sources</h4>
            <ul>
              {sources.map((s, i) => (
                <li key={i}>
                  {s.source} — score: {s.score.toFixed(2)}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f6fb",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Arial, sans-serif",
  },
  card: {
    background: "#ffffff",
    padding: "30px",
    width: "700px",
    borderRadius: "10px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
  },
  inputRow: {
    display: "flex",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "12px",
    fontSize: "16px",
  },
  button: {
    padding: "12px 20px",
    fontSize: "16px",
    cursor: "pointer",
  },
  loading: {
    marginTop: "15px",
    color: "#555",
  },
  error: {
    marginTop: "15px",
    color: "red",
  },
  answerBox: {
    marginTop: "25px",
    padding: "15px",
    background: "#03091cff",
    borderRadius: "8px",
  },
  sourcesBox: {
    marginTop: "15px",
    padding: "15px",
    background: "#030b14ff",
    borderRadius: "8px",
  },
};
