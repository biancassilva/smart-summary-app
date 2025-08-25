# Smart Summary App - Frontend

A modern Next.js 15 application for AI-powered text summarization with real-time streaming responses.

## 🏗️ Architecture

This application follows Next.js best practices with a clean, modular architecture:

```
src/
├── app/                    # Next.js 15 App Router
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable UI components
│   ├── chat/             # Chat-specific components
│   │   ├── ChatForm.tsx  # Message input form
│   │   ├── ChatResponse.tsx # AI response display
│   │   └── MarkdownRenderer.tsx # Markdown rendering
│   ├── layout/           # Layout components
│   │   └── Header.tsx    # Application header
│   └── ui/               # Generic UI components
│       ├── ErrorBoundary.tsx # Error handling
│       └── LoadingSpinner.tsx # Loading states
├── hooks/                # Custom React hooks
│   └── useChat.ts        # Chat state management
├── lib/                  # Utility functions
│   ├── api.ts           # API service layer
│   ├── markdown.ts      # Markdown preprocessing
│   └── utils.ts         # Common utilities
└── types/               # TypeScript definitions
    └── chat.ts          # Chat-related types
```

## 🚀 Features

- **Modern Architecture**: Built with Next.js 15, React 19, and TypeScript
- **Real-time Streaming**: Server-Sent Events for live AI responses
- **Markdown Support**: Full markdown rendering with syntax highlighting
- **Error Boundaries**: Robust error handling and recovery
- **Custom Hooks**: Reusable state management logic
- **Component Separation**: Clean, testable component architecture
- **Type Safety**: Full TypeScript coverage

## 🛠️ Development

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Setup

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.local.example .env.local
```

3. Start the development server:
```bash
npm run dev
```

### Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## 🏛️ Architecture Patterns

### Custom Hooks Pattern
The `useChat` hook encapsulates all chat-related state and logic:
```typescript
const { text, response, isStreaming, handleSubmit } = useChat();
```

### Service Layer Pattern
API calls are abstracted into a service layer:
```typescript
import { streamChatCompletion } from '@/lib/api';
```

### Component Composition
Components are small, focused, and composable:
```tsx
<ChatResponse response={response} isStreaming={isStreaming} />
```

### Error Boundaries
Graceful error handling at the component level:
```tsx
<ErrorBoundary>
  <ChatPage />
</ErrorBoundary>
```

## 🎨 Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first approach
- **Custom Components**: Consistent design system

## 📦 Dependencies

### Core
- `next` - React framework
- `react` - UI library  
- `typescript` - Type safety

### UI & Styling
- `tailwindcss` - CSS framework
- `clsx` - Conditional classes
- `react-markdown` - Markdown rendering

### Development
- `eslint` - Code linting
- `@types/*` - TypeScript definitions

## 🔧 Configuration

- `tsconfig.json` - TypeScript configuration with path mapping
- `tailwind.config.js` - Tailwind CSS configuration
- `next.config.js` - Next.js configuration
- `.env.local` - Environment variables

## 🚦 Best Practices Implemented

1. **Separation of Concerns**: Business logic separated from UI
2. **Custom Hooks**: Reusable state logic
3. **Type Safety**: Full TypeScript coverage
4. **Error Handling**: Comprehensive error boundaries
5. **Performance**: Optimized with Next.js features
6. **Accessibility**: ARIA labels and semantic HTML
7. **Code Organization**: Clear folder structure
8. **Environment Configuration**: Proper env var management

This architecture ensures maintainability, scalability, and follows modern React/Next.js conventions.