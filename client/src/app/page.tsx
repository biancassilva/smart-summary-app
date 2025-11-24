"use client";

import { useChat } from "@/hooks/useChat";
import { Header } from "@/components/layout/Header";
import { ChatForm } from "@/components/chat/ChatForm";
import { ResponsePanel } from "@/components/chat/ResponsePanel";
import { ErrorBoundary } from "@/components/ui/ErrorBoundary";

function ChatPage() {
  const {
    text,
    response,
    isStreaming,
    error,
    usage,
    model,
    isPanelOpen,
    handleTextChange,
    handleSubmit,
    closeSidePanel,
  } = useChat();

  return (
    <main className="min-h-screen bg-white">
      <div className="h-screen flex flex-col md:flex-row">
        {/* Mobile: Second column (Response Panel) appears first on mobile */}
        {isPanelOpen && (
          <div className="md:hidden w-full h-1/2 border-b border-gray-200 animate-fade-in animate-slide-in-from-top">
            <div className="bg-white h-full flex flex-col">
              <div className="flex items-center justify-between p-2 border-b border-gray-200 bg-gray-50">
                <h2 className="text-lg font-bold text-gray-900">
                  Summary Result
                </h2>
                <button
                  onClick={closeSidePanel}
                  className="p-2 bg-red-500 rounded-lg hover:bg-gray-100 transition-colors"
                  aria-label="Close panel"
                >
                  <svg
                    className="w-5 h-5 text-gray-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div className="flex-1 p-4 overflow-y-auto">
                <ResponsePanel
                  response={response}
                  isStreaming={isStreaming}
                  usage={usage}
                  model={model}
                />
              </div>
            </div>
          </div>
        )}

        {/* Left side - Input Form */}
        <div
          className={`transition-all duration-300 flex flex-col ${
            isPanelOpen ? "w-full h-1/2 md:w-1/2 md:h-full" : "w-full h-full"
          }`}
        >
          <div className="flex-1 flex items-center justify-center p-4">
            <div className="w-full max-w-4xl">
              <Header />
              <ChatForm
                text={text}
                isStreaming={isStreaming}
                error={error}
                onTextChange={handleTextChange}
                onSubmit={handleSubmit}
              />
            </div>
          </div>
        </div>

        {/* Desktop: Right side - Response Panel */}
        <div
          className={`hidden md:block transition-all duration-300 overflow-hidden ${
            isPanelOpen ? "w-1/2" : "w-0"
          }`}
        >
          {isPanelOpen && (
            <div className="bg-white border-l border-gray-200 h-full flex flex-col animate-fade-in animate-slide-in-from-right">
              <div className="flex items-center justify-between py-4 px-4 border-b border-gray-200 bg-gray-50">
                <h2 className="text-lg font-bold text-gray-900">
                  Summary Result
                </h2>
                <button
                  onClick={closeSidePanel}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  aria-label="Close panel"
                >
                  <svg
                    className="w-5 h-5 text-gray-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div className="flex-1 p-4 overflow-y-auto">
                <ResponsePanel
                  response={response}
                  isStreaming={isStreaming}
                  usage={usage}
                  model={model}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

export default function Page() {
  return (
    <ErrorBoundary>
      <ChatPage />
    </ErrorBoundary>
  );
}
