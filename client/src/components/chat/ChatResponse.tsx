import { MarkdownRenderer } from './MarkdownRenderer';
import { LoadingSpinner } from '../ui/LoadingSpinner';

interface ChatResponseProps {
  response: string;
  isStreaming: boolean;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  } | null;
  model?: string;
}

export function ChatResponse({ 
  response, 
  isStreaming, 
  usage, 
  model 
}: ChatResponseProps) {
  return (
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
            <LoadingSpinner size="sm" className="border-blue-600 mr-2" />
            Generating response...
          </div>
        ) : (
          <MarkdownRenderer content={response} isStreaming={isStreaming} />
        )}
      </div>
    </div>
  );
}