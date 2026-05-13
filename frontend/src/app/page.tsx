export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-[#f7f7f8]">
      {/* Header */}
      <header className="border-b border-neutral-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-4xl items-center px-6">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-neutral-400">
              Retrieval-Based Healthcare Assistant
            </p>

            <h1 className="text-lg font-semibold text-neutral-900">
              Medical RAG Assistant
            </h1>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <section className="flex-1 overflow-y-auto">
        <div className="mx-auto flex w-full max-w-4xl flex-col px-6 py-10">
          {/* Assistant Message */}
          <div className="mb-10 max-w-3xl">
            <p className="text-[15px] leading-8 text-neutral-700">
              Ask medical questions and receive answers grounded in trusted
              medical documents with source citations.
            </p>

            {/* Sources */}
            <div className="mt-6 flex flex-wrap gap-2">
              <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-600">
                WHO
              </span>

              <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-600">
                PubMed
              </span>
            </div>

            {/* Disclaimer */}
            <div className="mt-5">
              <span className="inline-flex items-center rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700 ring-1 ring-amber-100">
                Not a medical diagnosis
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Input */}
      <div className="sticky bottom-0 border-t border-neutral-200 bg-[#f7f7f8]/80 backdrop-blur">
        <div className="mx-auto w-full max-w-4xl px-6 py-6">
          <div className="relative overflow-hidden rounded-3xl border border-neutral-200 bg-white shadow-sm">
            <textarea
              placeholder="Ask a medical question..."
              className="min-h-[120px] w-full resize-none bg-transparent px-5 py-4 pr-28 text-[15px] text-neutral-800 placeholder:text-neutral-400 outline-none"
            />

            <div className="absolute bottom-4 right-4 flex items-center gap-3">
              <span className="hidden text-xs text-neutral-400 sm:block">
                Local document retrieval
              </span>

              <button className="rounded-2xl bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:opacity-90 active:scale-[0.98]">
                Ask
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
