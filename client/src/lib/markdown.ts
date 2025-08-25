/**
 * Preprocesses markdown text for better parsing by react-markdown
 * Ensures proper spacing around headings, lists, and other markdown elements
 */
export function preprocessMarkdown(text: string): string {
  if (!text) return text;

  return text
    // Ensure headings start on new lines
    .replace(/([^\n])(#{1,6}\s)/g, '$1\n\n$2')
    // Add space after # if missing
    .replace(/(#{1,6})([^\s#])/g, '$1 $2')
    // Ensure proper spacing after headings
    .replace(/(#{1,6}[^\n]+)\n([^\n\s])/g, '$1\n\n$2')
    // Fix bullet points
    .replace(/([^\n])(\*\s)/g, '$1\n$2')
    // Ensure paragraphs have proper spacing
    .replace(/([.!?])\s*([A-Z])/g, '$1\n\n$2');
}