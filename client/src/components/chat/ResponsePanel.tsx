"use client";

import { useEffect, useRef } from "react";
import { MarkdownRenderer } from "./MarkdownRenderer";
import { LoadingSpinner } from "../ui/LoadingSpinner";

interface ResponsePanelProps {
  response: string;
  isStreaming: boolean;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  } | null;
  model?: string;
}

export function ResponsePanel({
  response,
  isStreaming,
  usage,
  model,
}: ResponsePanelProps) {
  const contentRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new content arrives
  useEffect(() => {
    if (contentRef.current && response && isStreaming) {
      const element = contentRef.current;
      element.scrollTop = element.scrollHeight;
    }
  }, [response, isStreaming]);

  console.log("ResponsePanel render:", { response, isStreaming, usage, model });

  return (
    <div className="h-full flex flex-col">
      {/* Status Bar */}
      {!isStreaming ? (
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            {!isStreaming && response && (
              <div className="flex items-center gap-2 text-green-600">
                <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                <span className="text-sm font-medium">Complete</span>
              </div>
            )}
          </div>

          {usage && (
            <div className="text-sm text-gray-500 space-x-3">
              {model && (
                <span>
                  Model: <span className="font-medium">{model}</span>
                </span>
              )}
              <span>
                Tokens:{" "}
                <span className="font-medium">{usage.total_tokens}</span>
              </span>
            </div>
          )}
        </div>
      ) : null}

      {/* Content Area */}
      <div ref={contentRef} className="flex-1 overflow-y-auto scroll-smooth">
        {isStreaming && !response ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <LoadingSpinner size="lg" className="border-blue-600 mb-4" />
            <p className="text-lg">Preparing your summary...</p>
            <p className="text-sm text-gray-400 mt-2">
              This may take a few moments
            </p>
          </div>
        ) : (
          <div className="prose prose-slate max-w-none">
            <MarkdownRenderer content={response} isStreaming={isStreaming} />
          </div>
        )}
      </div>

      {/* Footer */}
      {response && !isStreaming && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <div className="flex justify-between items-center text-xs text-gray-400">
            <span>Summary generated successfully</span>
            <span>{new Date().toLocaleTimeString()}</span>
          </div>
        </div>
      )}
    </div>
  );
}
