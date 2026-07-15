import { useState } from "react";
import type { FormEvent } from "react";
import "./App.css";

type Tone = "professional" | "friendly" | "concise" | "confident" | "polite";

type RequestStatus = "idle" | "streaming" | "success" | "error";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const API_URL = `${API_BASE_URL}/api/rewrite/stream`;

function App() {
  const [email, setEmail] = useState("");
  const [tone, setTone] = useState<Tone>("professional");
  const [rewrittenEmail, setRewrittenEmail] = useState("");
  const [status, setStatus] = useState<RequestStatus>("idle");
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  async function handleRewrite(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!email.trim()) {
      setError("Please enter an email to rewrite.");
      setStatus("error");
      return;
    }

    setStatus("streaming");
    setError("");
    setRewrittenEmail("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          tone,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to rewrite the email.");
      }

      if (!response.body) {
        throw new Error("Streaming is not supported by this browser.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });

        setRewrittenEmail((current) => current + chunk);
      }

      setStatus("success");
    } catch (caughtError) {
      const message =
        caughtError instanceof Error
          ? caughtError.message
          : "Something went wrong.";

      setError(message);
      setStatus("error");
    }
  }

  async function handleCopy() {
    if (!rewrittenEmail) {
      return;
    }

    await navigator.clipboard.writeText(rewrittenEmail);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <main>
      <header className="app-header">
        <h1>AI Email Rewriter</h1>
        <p>
          Rewrite emails with better tone, grammar, and clarity while preserving
          your original meaning.
        </p>
      </header>

      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}

      <div className="workspace">
        <form className="panel" onSubmit={handleRewrite}>
          <div className="panel-header">
            <h2>Original email</h2>
            <p>Paste your draft and choose the tone you want.</p>
          </div>

          <div className="form-group output-area">
            <label htmlFor="email">Email content</label>

            <textarea
              id="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="Paste or type your email here..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="tone">Tone</label>

            <select
              id="tone"
              value={tone}
              onChange={(event) => setTone(event.target.value as Tone)}
            >
              <option value="professional">Professional</option>
              <option value="friendly">Friendly</option>
              <option value="concise">Concise</option>
              <option value="confident">Confident</option>
              <option value="polite">Polite</option>
            </select>
          </div>

          <button
            className="primary-button"
            type="submit"
            disabled={status === "streaming"}
          >
            {status === "streaming" ? "Rewriting..." : "Rewrite email"}
          </button>
        </form>

        <section className="output-box">
          <div className="panel-header">
            <h2>Rewritten email</h2>
            <p>Your improved version will appear here as it is generated.</p>
          </div>

          {status === "streaming" && !rewrittenEmail && (
            <p className="status-message">Improving tone and clarity...</p>
          )}

          <div className="output-box">
            {rewrittenEmail ? (
              <p className="output-text">
                {rewrittenEmail}
                {status === "streaming" && (
                  <span className="streaming-cursor">▌</span>
                )}
              </p>
            ) : (
              <div className="empty-state">
                <span className="empty-state-icon">✨</span>
                <h3>Your improved email will appear here</h3>
                <p>
                  We’ll preserve your meaning, improve clarity, and match your
                  selected tone.
                </p>
              </div>
            )}
          </div>

          <button
            className="secondary-button"
            type="button"
            onClick={handleCopy}
            disabled={!rewrittenEmail || status === "streaming"}
          >
            {copied ? "✓ Copied!" : "Copy Email"}
          </button>
        </section>
      </div>
    </main>
  );
}

export default App;
