import ReactMarkdown from 'react-markdown';
import { preprocessMarkdown } from '@/lib/markdown';

interface MarkdownRendererProps {
  content: string;
  isStreaming?: boolean;
}

export function MarkdownRenderer({ content, isStreaming }: MarkdownRendererProps) {
  return (
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
        {preprocessMarkdown(content)}
      </ReactMarkdown>
      {isStreaming && (
        <span className="inline-block w-2 h-4 bg-blue-600 ml-1 animate-pulse" />
      )}
    </div>
  );
}