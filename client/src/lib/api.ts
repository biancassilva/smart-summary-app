import { StreamChunk } from "@/types/chat";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export interface ChatStreamOptions {
  message: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  conversation_history?: any[];
  stream?: boolean;
  onChunk?: (chunk: StreamChunk) => void;
  onComplete?: () => void;
  onError?: (error: ApiError) => void;
}

export async function streamChatCompletion({
  message,
  conversation_history = [],
  stream = true,
  onChunk,
  onComplete,
  onError,
}: ChatStreamOptions): Promise<void> {
  try {
    console.log("🚀 Starting streamChatCompletion with message:", message);

    const response = await fetch(`${API_BASE_URL}/api/v1/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        conversation_history,
        stream,
      }),
    });

    console.log("📡 Response status:", response.status, response.statusText);

    if (!response.ok) {
      throw new ApiError(
        `Failed to start streaming: ${response.status} ${response.statusText}`,
        response.status,
        response.statusText
      );
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new ApiError("No response body", 500, "Internal Server Error");
    }

    const decoder = new TextDecoder();

    console.log("🔄 Starting to read stream...");

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        console.log("✅ Stream reading completed");
        onComplete?.();
        break;
      }

      const chunk = decoder.decode(value);
      console.log("📦 Raw chunk received:", chunk);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataContent = line.slice(6).trim();

          if (dataContent === "[DONE]") {
            console.log("🏁 Received [DONE] signal");
            onComplete?.();
            return;
          }

          if (dataContent === "") {
            continue;
          }

          try {
            const data: StreamChunk = JSON.parse(dataContent);

            if (data.content || data.is_complete) {
              onChunk?.(data);
            }

            if (data.is_complete) {
              console.log("✅ Stream marked as complete");
              onComplete?.();
              return;
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
                throw new ApiError(
                  errorData.error?.message || "An error occurred",
                  errorData.error?.status_code || 500,
                  "Server Error"
                );
              } catch {
                throw new ApiError(
                  "Failed to parse error response",
                  500,
                  "Parse Error"
                );
              }
            }
          }
        }
      }
    }
  } catch (err) {
    console.error("🚨 StreamChatCompletion error:", err);

    if (err instanceof ApiError) {
      onError?.(err);
    } else {
      onError?.(
        new ApiError(
          err instanceof Error ? err.message : "Streaming failed",
          500,
          "Unknown Error"
        )
      );
    }
  }
}
