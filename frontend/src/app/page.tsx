"use client";

import { useState } from "react";

type Source = {
  title: string;
  source: string;
  year: string;
  page: number;
  url: string;
  score: number;
};

type ApiResponse = {
  answer: string;
  confidence: {
    label: string;
    value: number;
  };
  refused: boolean;
  sources: Source[];
  warning: string;
};

export default function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Failed to get response from backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen flex-col bg-[#f7f7f8]">
      <header className="border-b border-neutral-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-4xl items-center px-6">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-neutral-400">
              Evidence-Grounded Clinical Assistant
            </p>
            <h1 className="text-lg font-semibold text-neutral-900">
              Medical RAG Assistant
            </h1>
          </div>
        </div>
      </header>

      <section className="flex-1 overflow-y-auto">
        <div className="mx-auto flex w-full max-w-4xl flex-col px-6 py-10">
          <div className="mb-8 max-w-3xl">
            <p className="text-[15px] leading-8 text-neutral-700">
              Ask clinical questions and receive answers grounded in retrieved
              medical guideline evidence with source citations.
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-600">
                FAISS Retrieval
              </span>
              <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-600">
                Groq LLM
              </span>
              <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-600">
                Citation-Aware
              </span>
            </div>

            <div className="mt-5">
              <span className="inline-flex items-center rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700 ring-1 ring-amber-100">
                Not a medical diagnosis
              </span>
            </div>
          </div>

          {result && (
            <div className="space-y-5">
              <div className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
                <div className="mb-4 flex items-center gap-3">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-medium ${
                      result.refused
                        ? "bg-red-50 text-red-700 ring-1 ring-red-100"
                        : "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100"
                    }`}
                  >
                    {result.refused ? "Refused" : "Answered"}
                  </span>

                  <span className="rounded-full bg-neutral-100 px-3 py-1 text-xs font-medium text-neutral-700">
                    Confidence: {result.confidence?.label}
                  </span>
                </div>

                <div
                  className="whitespace-pre-wrap text-[15px] leading-8 text-neutral-800"
                  dangerouslySetInnerHTML={{
                    __html: result.answer
                      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                      .replace(/\n/g, "<br />"),
                  }}
                />

                <p className="mt-5 text-xs text-neutral-500">
                  {result.warning}
                </p>
              </div>

              {result.sources?.length > 0 && (
                <div className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
                  <h2 className="mb-4 text-sm font-semibold text-neutral-900">
                    Evidence Sources
                  </h2>

                  <div className="space-y-3">
                    {result.sources.map((source, index) => (
                      <div
                        key={`${source.title}-${index}`}
                        className="rounded-2xl border border-neutral-100 bg-neutral-50 p-4"
                      >
                        <p className="text-sm font-medium text-neutral-900">
                          {source.title}
                        </p>
                        <p className="mt-1 text-xs text-neutral-500">
                          {source.source} · {source.year} · Page {source.page}
                        </p>
                        {source.url && (
                          <p className="mt-1 text-xs text-neutral-500">
                            {source.url}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      <div className="sticky bottom-0 border-t border-neutral-200 bg-[#f7f7f8]/80 backdrop-blur">
        <div className="mx-auto w-full max-w-4xl px-6 py-6">
          <div className="relative overflow-hidden rounded-3xl border border-neutral-200 bg-white shadow-sm">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a clinical question..."
              className="min-h-[120px] w-full resize-none bg-transparent px-5 py-4 pr-28 text-[15px] text-neutral-800 placeholder:text-neutral-400 outline-none"
            />

            <div className="absolute bottom-4 right-4 flex items-center gap-3">
              <button
                onClick={handleAsk}
                disabled={loading}
                className="rounded-2xl bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:opacity-90 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Thinking..." : "Ask"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
