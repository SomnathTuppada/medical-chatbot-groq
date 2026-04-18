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
      <div style={styles.container}>
        
        <h1 style={styles.title}>🧠 Medical RAG Chatbot</h1>

        <div style={styles.chatBox}>
          {answer && (
            <div style={styles.answerBox}>
              <p>{answer}</p>
            </div>
          )}

          {loading && <p style={styles.loading}>Thinking...</p>}
          {error && <p style={styles.error}>{error}</p>}
        </div>

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
          <div style={styles.footer}>
            Built by Somnath Tuppada
          </div>
        </div>

      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    width: "100vw",
    background: "#0b0f19", // full dark background
    color: "#ffffff",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Arial, sans-serif",
  },

  container: {
    width: "90%",
    maxWidth: "900px",
    height: "90vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
  },

  title: {
    textAlign: "center",
    fontSize: "32px",
    marginBottom: "10px",
  },

  chatBox: {
    flex: 1,
    overflowY: "auto",
    padding: "20px",
    background: "#111827",
    borderRadius: "10px",
    marginBottom: "10px",
  },

  answerBox: {
    background: "#1f2937",
    padding: "15px",
    borderRadius: "8px",
    lineHeight: "1.6",
  },

  sourcesBox: {
    background: "#111827",
    padding: "10px",
    borderRadius: "8px",
    marginBottom: "10px",
    fontSize: "14px",
    color: "#cbd5e1",
  },

  inputRow: {
    display: "flex",
    gap: "10px",
  },

  input: {
    flex: 1,
    padding: "12px",
    fontSize: "16px",
    borderRadius: "6px",
    border: "none",
    outline: "none",
    background: "#1f2937",
    color: "#fff",
  },

  button: {
    padding: "12px 20px",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },

  loading: {
    color: "#9ca3af",
  },

  error: {
    color: "#ef4444",
  },
  footer: {
    position: "fixed",
    bottom: "10px",
    right: "20px",
    color: "#9ca3af",
    fontSize: "14px",
    opacity: 0.8,
  },
};