import asyncio
import time
from typing import Optional
import structlog
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

logger = structlog.get_logger()


class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def summarize_text(self, text: str) -> tuple[str, float]:
        """
        Summarize text using OpenAI API

        Returns:
            tuple[str, float]: (summary, processing_time)
        """
        start_time = time.time()

        try:
            prompt = self._create_summary_prompt(text)

            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates concise, informative summaries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE,
                timeout=30.0,
            )

            summary = response.choices[0].message.content.strip()
            processing_time = time.time() - start_time

            logger.info(
                "Text summarized successfully",
                text_length=len(text),
                summary_length=len(summary),
                processing_time=processing_time,
                model=settings.OPENAI_MODEL,
            )

            return summary, processing_time

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                "Failed to summarize text",
                error=str(e),
                text_length=len(text),
                processing_time=processing_time,
            )
            raise

    def _create_summary_prompt(self, text: str) -> str:
        """Create a prompt for text summarization"""
        return f"""
Please provide a concise summary of the following text. The summary should:
- Capture the main points and key information
- Be significantly shorter than the original text
- Maintain the essential meaning and context
- Be clear and easy to understand

Text to summarize:
{text}

Summary:
        """.strip()
