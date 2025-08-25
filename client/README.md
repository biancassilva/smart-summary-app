# EasyMate Client

A Next.js application for AI-powered text summarization, built with Tailwind CSS v4.

## Features

- Clean, modern UI with Tailwind CSS
- Text input with character validation (50-50,000 characters)
- Integration with EasyMate backend API
- Real-time status updates for summary generation
- Responsive design for all devices

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- EasyMate backend running on `http://localhost:8000`

### Installation

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Paste your text (article, meeting notes, email, etc.) into the textarea
2. Ensure the text is between 50 and 50,000 characters
3. Click "Generate Summary" to send the text to the backend
4. View the generated summary or any error messages

## API Integration

The application integrates with the EasyMate backend API:

- **Endpoint**: `POST /api/v1/summaries/`
- **Request Body**: `{ "text": "your text here" }`
- **Response**: Summary object with status, text, and metadata

## Technologies Used

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Utility-first CSS framework
- **React 19** - UI library

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── app/
│   ├── globals.css      # Global styles with Tailwind
│   ├── layout.tsx       # Root layout component
│   └── page.tsx         # Home page with text input
└── ...
```
