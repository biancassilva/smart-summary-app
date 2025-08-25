import asyncio
import logging
from typing import AsyncGenerator, List, Optional
import google.generativeai as genai
from app.core.config import settings
from app.core.exceptions import OpenAIServiceException
from app.schemas.chat import ChatMessage, StreamingChatResponse

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for Google Gemini API interactions"""

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.default_model = settings.GEMINI_MODEL
        self.default_max_tokens = settings.GEMINI_MAX_TOKENS
        self.default_temperature = settings.GEMINI_TEMPERATURE

    def _prepare_messages(
        self, user_message: str, conversation_history: List[ChatMessage]
    ) -> str:
        """Prepare messages for Gemini API with markdown formatting instructions"""
        
        # System instruction for summary-focused responses with markdown formatting
        markdown_instructions = """You are an AI summarization assistant that specializes in creating clear, concise summaries from text blocks. Your primary goal is to extract key information and present it in well-formatted markdown.

**YOUR MAIN PURPOSE:**
- Transform articles, meeting notes, emails, and documents into digestible summaries
- Extract key points, main ideas, and actionable items
- Present information in a structured, easy-to-read format

**FORMATTING REQUIREMENTS:**
- Use headings: # Main Summary, ## Key Points, ### Details, #### Action Items
- Format text: **bold** for key terms, *italic* for emphasis
- Use `inline code` for technical terms, file names, or specific values
- Make bulleted lists with - or * for key points and findings
- Make numbered lists with 1. 2. 3. for sequential steps or priorities
- Use > blockquotes for important quotes or critical information
- Create tables with | headers | data | when organizing structured data
- Add horizontal rules --- to separate major sections

**SUMMARY STRUCTURE:**
1. **# Summary** - Start with a clear title describing the content type
2. **## Key Points** - Extract 3-5 main takeaways using bullet points
3. **## Details** - Provide supporting information in subsections as needed
4. **## Action Items** (if applicable) - List any tasks, decisions, or next steps
5. **## Conclusion** - Brief wrap-up of the most important information

**CONTENT HANDLING:**
- For **articles**: Focus on main arguments, findings, and conclusions
- For **meeting notes**: Highlight decisions made, action items, and key discussions
- For **emails**: Summarize purpose, requests, deadlines, and required responses
- For **documents**: Extract core concepts, important data, and recommendations

Always format your response using rich markdown to make the summary clear and scannable:

"""
        
        # Combine system instructions with conversation
        full_conversation = markdown_instructions
        
        # Add conversation history
        for msg in conversation_history:
            if msg.role == "user":
                full_conversation += f"\nUser: {msg.content}"
            elif msg.role == "assistant":
                full_conversation += f"\nAssistant: {msg.content}"
        
        # Add current user message
        full_conversation += f"\nUser: {user_message}\nAssistant: "
        
        return full_conversation

    async def chat_completion(
        self,
        user_message: str,
        conversation_history: List[ChatMessage] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        """Get chat completion from Gemini (non-streaming)"""
        try:
            prompt = self._prepare_messages(user_message, conversation_history or [])
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature or self.default_temperature,
                max_output_tokens=max_tokens or self.default_max_tokens,
            )
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config
            )

            return {
                "content": response.text,
                "model": model or self.default_model,
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(response.text.split()),
                    "total_tokens": len(prompt.split()) + len(response.text.split()),
                },
            }

        except Exception as e:
            logger.error(f"Unexpected error in chat_completion: {str(e)}")
            raise OpenAIServiceException(f"Failed to get chat completion: {str(e)}", 500)

    async def chat_completion_stream(
        self,
        user_message: str,
        conversation_history: List[ChatMessage] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[StreamingChatResponse, None]:
        """Get streaming chat completion from Gemini"""
        logger.info(f"Starting Gemini streaming for message: {user_message[:100]}...")
        
        try:
            prompt = self._prepare_messages(user_message, conversation_history or [])
            logger.debug(f"Prepared prompt length: {len(prompt)} characters")
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature or self.default_temperature,
                max_output_tokens=max_tokens or self.default_max_tokens,
            )
            logger.debug(f"Generation config: temp={generation_config.temperature}, max_tokens={generation_config.max_output_tokens}")
            
            current_model = model or self.default_model
            logger.info(f"Using model: {current_model}")
            
            # Generate content with streaming
            logger.info("Creating Gemini streaming response...")
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            full_content = ""
            chunk_count = 0
            
            logger.info("Starting to iterate through response chunks...")
            for chunk in response:
                chunk_count += 1
                logger.debug(f"Processing chunk #{chunk_count}")
                
                if hasattr(chunk, 'text') and chunk.text:
                    content = chunk.text
                    full_content += content
                    logger.debug(f"Chunk content: '{content[:50]}...' (length: {len(content)})")
                    
                    # Break content into smaller chunks for more granular streaming
                    words = content.split()
                    chunk_size = settings.STREAMING_CHUNK_SIZE
                    delay_seconds = settings.STREAMING_DELAY_MS / 1000.0
                    
                    if len(words) > chunk_size:  # If chunk has more words than chunk_size, break it down
                        # Send words in groups based on STREAMING_CHUNK_SIZE
                        word_groups = []
                        i = 0
                        while i < len(words):
                            group = words[i:i+chunk_size]
                            word_groups.append(" ".join(group) + (" " if i + chunk_size < len(words) else ""))
                            i += chunk_size
                        
                        # Yield each word group as a separate chunk
                        for word_group in word_groups:
                            response_obj = StreamingChatResponse(
                                content=word_group,
                                is_complete=False,
                                model=current_model
                            )
                            logger.debug(f"Yielding word group: '{word_group}'")
                            yield response_obj
                            
                            # Add configurable delay for streaming effect
                            await asyncio.sleep(delay_seconds)
                    else:
                        # For small chunks, send as is
                        response_obj = StreamingChatResponse(
                            content=content,
                            is_complete=False,
                            model=current_model
                        )
                        logger.debug(f"Yielding streaming response: {response_obj}")
                        yield response_obj
                        await asyncio.sleep(delay_seconds)  # Consistent delay for better UX
                else:
                    logger.warning(f"Chunk #{chunk_count} has no text content")
            
            logger.info(f"Streaming completed. Total chunks: {chunk_count}, Total content length: {len(full_content)}")
            
            # Send completion signal
            completion_response = StreamingChatResponse(
                content="",
                is_complete=True,
                model=current_model,
                usage={
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(full_content.split()),
                    "total_tokens": len(prompt.split()) + len(full_content.split())
                }
            )
            logger.info(f"Sending completion signal: {completion_response}")
            yield completion_response

        except Exception as e:
            logger.error(f"Unexpected error in chat_completion_stream: {str(e)}", exc_info=True)
            raise OpenAIServiceException(f"Failed to get streaming chat completion: {str(e)}", 500)