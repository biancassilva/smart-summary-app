import { LoadingSpinner } from '../ui/LoadingSpinner';

interface ChatFormProps {
  text: string;
  isStreaming: boolean;
  error: string | null;
  onTextChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function ChatForm({
  text,
  isStreaming,
  error,
  onTextChange,
  onSubmit,
}: ChatFormProps) {
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <div>
        <textarea
          id="text"
          value={text}
          onChange={(e) => onTextChange(e.target.value)}
          placeholder="Type your message here (ask for summaries, explanations, or any help)..."
          className="bg-white w-full h-32 p-4 border border-black rounded-lg text-black focus:outline-none focus:border-black resize-none"
          disabled={isStreaming}
          aria-label="Chat input"
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
            <LoadingSpinner size="sm" className="border-white" />
            Generating Response...
          </>
        ) : (
          <>Generate Summary</>
        )}
      </button>
    </form>
  );
}