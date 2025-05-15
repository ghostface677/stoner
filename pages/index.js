import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setAnswer("");
    const res = await fetch("/api/completion", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: input }),
    });
    const data = await res.json();
    setAnswer(data.result);
    setLoading(false);
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Biomedical Troubleshooting Chatbot</h1>
      <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
        <input
          className="border p-2 rounded w-80"
          placeholder="Ask about biomedical equipment..."
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit" disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>
      <div className="bg-gray-100 rounded p-4 w-96 min-h-[100px]">
        {answer || "Your answer will appear here."}
      </div>
    </main>
  );
}
