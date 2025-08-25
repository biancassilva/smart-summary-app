/**
 * Preprocesses markdown text for better parsing by react-markdown
 * Ensures proper spacing around headings, lists, and other markdown elements
 * Fixes malformed bullet points and list formatting
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
    
    // Fix malformed bullet points - convert *text to proper markdown lists
    .replace(/^(\*\s*([A-Z].*?))\n/gm, '- $2\n')
    // Fix bullet points that don't start at line beginning
    .replace(/([^\n])(\*\s*([A-Z].*?))\n/gm, '$1\n- $3\n')
    // Fix inline asterisks that should be bullet points
    .replace(/([^\n]\s+)(\*(?=[A-Z]))/g, '$1\n- ')
    
    // Ensure proper list formatting with blank lines
    .replace(/(^- .*$)(?=\n[^-\s])/gm, '$1\n')
    // Add blank line before lists
    .replace(/([^\n]\n)(- )/g, '$1\n$2')
    
    // Fix numbered lists
    .replace(/^(\d+\.\s*([A-Z].*?))\n/gm, '$1\n')
    
    // Ensure paragraphs have proper spacing
    .replace(/([.!?])\s*([A-Z][^.!?\n]*[.!?])/g, '$1\n\n$2')
    
    // Clean up extra whitespace
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}