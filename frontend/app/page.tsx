"use client";

import { useState } from "react";

type Reply = {
  character_id: number;
  character_name: string;
  reply: string;
};

type DiscussionResponse = {
  user_message: string;
  replies: Reply[];
  summary: string;
};

type ChatMessage = {
  id: string;
  sender: "user" | "character" | "summary";
  name?: string;
  text: string;
};

export default function Home() {
  const [userMessage, setUserMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!userMessage.trim()) return;

    const currentMessage = userMessage;

    const userChat: ChatMessage = {
      id: crypto.randomUUID(),
      sender: "user",
      text: currentMessage,
    };

    setMessages((prev) => [...prev, userChat]);
    setUserMessage("");
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/discussion", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_message: currentMessage,
        }),
      });

      if (!res.ok) {
        throw new Error("API request failed");
      }

      const json: DiscussionResponse = await res.json();

      const replyMessages: ChatMessage[] = json.replies.map((reply) => ({
        id: crypto.randomUUID(),
        sender: "character",
        name: reply.character_name,
        text: reply.reply,
      }));

      const summaryMessage: ChatMessage = {
        id: crypto.randomUUID(),
        sender: "summary",
        name: "まとめ",
        text: json.summary,
      };

      setMessages((prev) => [
        ...prev,
        ...replyMessages,
        summaryMessage,
      ]);
    } catch (err) {
      console.error(err);
      setError("会話の取得に失敗しました。バックエンドやOllamaの起動状態を確認してください。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col bg-slate-100">
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <div className="mx-auto max-w-4xl">
          <h1 className="text-2xl font-bold text-slate-900">CharaAgent</h1>
          <p className="mt-1 text-sm text-slate-500">
            キャラクターたちが順番に議論して返答するチャット
          </p>
        </div>
      </header>

      <section className="flex-1 overflow-y-auto px-4 py-6">
        <div className="mx-auto flex max-w-4xl flex-col gap-4">
          {messages.length === 0 && (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">
              まだ会話はありません。下の入力欄から質問してみてください。
            </div>
          )}

          {messages.map((message) => {
            if (message.sender === "user") {
              return (
                <div key={message.id} className="flex justify-end">
                  <div className="max-w-[75%] rounded-2xl rounded-br-md bg-slate-900 px-4 py-3 text-sm leading-7 text-white shadow-sm">
                    {message.text}
                  </div>
                </div>
              );
            }

            if (message.sender === "summary") {
              return (
                <div key={message.id} className="flex justify-center">
                  <div className="w-full max-w-3xl rounded-2xl border border-sky-200 bg-sky-50 px-5 py-4 shadow-sm">
                    <p className="mb-2 text-sm font-semibold text-sky-700">
                      {message.name}
                    </p>
                    <p className="text-sm leading-7 text-slate-700">
                      {message.text}
                    </p>
                  </div>
                </div>
              );
            }

            return (
              <div key={message.id} className="flex justify-start">
                <div className="max-w-[75%] rounded-2xl rounded-bl-md bg-white px-4 py-3 shadow-sm">
                  <p className="mb-1 text-xs font-semibold text-slate-500">
                    {message.name}
                  </p>
                  <p className="text-sm leading-7 text-slate-800">
                    {message.text}
                  </p>
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="flex justify-start">
              <div className="max-w-[75%] rounded-2xl rounded-bl-md bg-white px-4 py-3 shadow-sm">
                <p className="mb-1 text-xs font-semibold text-slate-500">
                  CharaAgent
                </p>
                <p className="text-sm text-slate-500">議論中...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}
        </div>
      </section>

      <footer className="border-t border-slate-200 bg-white px-4 py-4">
        <div className="mx-auto max-w-4xl">
          <div className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm sm:flex-row">
            <textarea
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              placeholder="質問を入力してください"
              className="min-h-[56px] flex-1 resize-none rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-slate-400"
            />
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-medium text-white disabled:opacity-50"
            >
              {loading ? "送信中..." : "送信"}
            </button>
          </div>
        </div>
      </footer>
    </main>
  );
}