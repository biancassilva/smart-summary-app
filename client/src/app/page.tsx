"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

interface StreamChunk {
  content: string;
  is_complete: boolean;
  model: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export default function Home() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [responseVisible, setResponseVisible] = useState(false);
  const [usage, setUsage] = useState<{
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  } | null>(null);
  const [model, setModel] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!text.trim()) {
      setError("Please enter some text");
      return;
    }

    if (isStreaming) {
      return;
    }

    setError(null);
    setResponse("");
    setUsage(null);
    setModel("");
    setResponseVisible(true);

    try {
      await streamResponse(text.trim());
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setResponseVisible(false);
    }
  };

  const streamResponse = async (message: string) => {
    console.log("🚀 Starting streamResponse with message:", message);

    setIsStreaming(true);
    setResponse("");

    try {
      console.log("📡 Making fetch request to streaming endpoint...");

      const fetchResponse = await fetch(
        "http://localhost:8000/api/v1/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
            conversation_history: [],
            stream: true,
          }),
        }
      );

      console.log(
        "📡 Response status:",
        fetchResponse.status,
        fetchResponse.statusText
      );

      if (!fetchResponse.ok) {
        throw new Error(
          `Failed to start streaming: ${fetchResponse.status} ${fetchResponse.statusText}`
        );
      }

      const reader = fetchResponse.body?.getReader();
      if (!reader) {
        throw new Error("No response body");
      }

      const decoder = new TextDecoder();
      let fullContent = "";

      console.log("🔄 Starting to read stream...");
      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          console.log("✅ Stream reading completed");
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataContent = line.slice(6).trim();

            if (dataContent === "[DONE]") {
              console.log("🏁 Received [DONE] signal");
              setIsStreaming(false);
              break;
            }

            if (dataContent === "") {
              continue;
            }

            try {
              const data: StreamChunk = JSON.parse(dataContent);

              if (data.content) {
                fullContent += data.content;
                setResponse(fullContent);
                setModel(data.model);
              }

              if (data.is_complete) {
                console.log("✅ Stream marked as complete");
                setUsage(data.usage || null);
                setIsStreaming(false);
                break;
              }
            } catch (parseError) {
              console.error(
                "❌ Failed to parse JSON:",
                parseError,
                "Data:",
                dataContent
              );

              if (dataContent.includes("error")) {
                try {
                  const errorData = JSON.parse(dataContent);
                  console.error("🚨 Error data:", errorData);
                  setError(errorData.error?.message || "An error occurred");
                } catch {
                  setError("Failed to parse error response");
                }
              }
            }
          }
        }
      }
    } catch (err) {
      console.error("🚨 StreamResponse error:", err);
      setError(err instanceof Error ? err.message : "Streaming failed");
      setIsStreaming(false);
      setResponseVisible(false);
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    setError(null);
  };

  // Function to preprocess markdown for better parsing
  const preprocessMarkdown = (text: string) => {
    if (!text) return text;

    return (
      text
        // Ensure headings start on new lines
        .replace(/([^\n])(#{1,6}\s)/g, "$1\n\n$2")
        // Add space after # if missing
        .replace(/(#{1,6})([^\s#])/g, "$1 $2")
        // Ensure proper spacing after headings
        .replace(/(#{1,6}[^\n]+)\n([^\n\s])/g, "$1\n\n$2")
        // Fix bullet points
        .replace(/([^\n])(\*\s)/g, "$1\n$2")
        // Ensure paragraphs have proper spacing
        .replace(/([.!?])\s*([A-Z])/g, "$1\n\n$2")
    );
  };

  return (
    <main className="min-h-screen bg-white flex items-center justify-center py-12 px-4">
      <div className="max-w-4xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Smart Summary App
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered assistant for summaries, explanations, and more.
          </p>
        </div>

        {/* Response Area - Shows above input after user sends message */}
        {responseVisible && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">AI Response</h2>
              {usage && (
                <div className="text-sm text-gray-500 space-x-3">
                  {model && <span>Model: {model}</span>}
                  <span>Tokens: {usage.total_tokens}</span>
                </div>
              )}
            </div>

            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
              {isStreaming && !response ? (
                <div className="flex items-center text-gray-500">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                  Generating response...
                </div>
              ) : (
                <div className="max-w-none">
                  <ReactMarkdown
                    components={{
                      // Custom styling for markdown elements with !important to override any conflicts
                      h1: ({ children }) => (
                        <h1 className="!text-3xl !font-bold !text-gray-900 !mb-6 !mt-8 !leading-tight">
                          {children}
                        </h1>
                      ),
                      h2: ({ children }) => (
                        <h2 className="!text-2xl !font-bold !text-gray-900 !mb-4 !mt-6 !leading-tight">
                          {children}
                        </h2>
                      ),
                      h3: ({ children }) => (
                        <h3 className="!text-xl !font-semibold !text-gray-900 !mb-3 !mt-5 !leading-tight">
                          {children}
                        </h3>
                      ),
                      h4: ({ children }) => (
                        <h4 className="!text-lg !font-semibold !text-gray-900 !mb-2 !mt-4 !leading-tight">
                          {children}
                        </h4>
                      ),
                      h5: ({ children }) => (
                        <h5 className="!text-base !font-semibold !text-gray-900 !mb-2 !mt-3 !leading-tight">
                          {children}
                        </h5>
                      ),
                      h6: ({ children }) => (
                        <h6 className="!text-sm !font-semibold !text-gray-900 !mb-1 !mt-2 !leading-tight !uppercase !tracking-wide">
                          {children}
                        </h6>
                      ),
                      p: ({ children }) => (
                        <p className="text-gray-900 leading-relaxed mb-4 text-justify">
                          {children}
                        </p>
                      ),
                      strong: ({ children }) => (
                        <strong className="font-semibold text-gray-900">
                          {children}
                        </strong>
                      ),
                      em: ({ children }) => (
                        <em className="italic text-gray-700">{children}</em>
                      ),
                      ul: ({ children }) => (
                        <ul className="list-disc list-inside mb-3 text-gray-900">
                          {children}
                        </ul>
                      ),
                      ol: ({ children }) => (
                        <ol className="list-decimal list-inside mb-3 text-gray-900">
                          {children}
                        </ol>
                      ),
                      li: ({ children }) => (
                        <li className="mb-1">{children}</li>
                      ),
                      code: ({ children, ...props }) => {
                        return (
                          <code
                            className="bg-gray-200 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono"
                            {...props}
                          >
                            {children}
                          </code>
                        );
                      },
                      blockquote: ({ children }) => (
                        <blockquote className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50 text-gray-700 mb-3">
                          {children}
                        </blockquote>
                      ),
                      a: ({ children, href }) => (
                        <a
                          href={href}
                          className="text-blue-600 hover:text-blue-800 underline"
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          {children}
                        </a>
                      ),
                      table: ({ children }) => (
                        <table className="min-w-full border-collapse border border-gray-300 mb-3">
                          {children}
                        </table>
                      ),
                      th: ({ children }) => (
                        <th className="border border-gray-300 px-4 py-2 bg-gray-100 font-semibold text-left">
                          {children}
                        </th>
                      ),
                      td: ({ children }) => (
                        <td className="border border-gray-300 px-4 py-2">
                          {children}
                        </td>
                      ),
                    }}
                  >
                    {preprocessMarkdown(response)}
                  </ReactMarkdown>
                  {isStreaming && (
                    <span className="inline-block w-2 h-4 bg-blue-600 ml-1 animate-pulse"></span>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Main Input Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <textarea
              id="text"
              value={text}
              onChange={handleTextChange}
              placeholder="Type your message here (ask for summaries, explanations, or any help)..."
              className="bg-white w-full h-32 p-4 border border-black rounded-lg text-black focus:outline-none focus:border-black resize-none"
              disabled={isStreaming}
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={!text.trim() || isStreaming}
            className="w-full border border-black text-black py-3 px-6 rounded-lg font-medium hover:bg-gray-100 focus:ring-0 cursor-pointer focus:ring-offset-0 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {isStreaming ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Generating Response...
              </>
            ) : (
              <>Generate Summary</>
            )}
          </button>
        </form>
      </div>
    </main>
  );
}
