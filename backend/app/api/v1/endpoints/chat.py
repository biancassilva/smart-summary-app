import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from app.api.dependencies import get_gemini_service
from app.services.gemini_service import GeminiService
from app.schemas.chat import ChatRequest, ChatResponse, StreamingChatResponse
from app.core.exceptions import OpenAIServiceException
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest, gemini_service: GeminiService = Depends(get_gemini_service)
):
    """Get chat completion (non-streaming)"""
    try:
        if request.stream:
            raise HTTPException(
                status_code=400,
                detail="Use /chat/stream endpoint for streaming responses",
            )

        result = await gemini_service.chat_completion(
            user_message=request.message,
            conversation_history=request.conversation_history,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return ChatResponse(
            response=result["content"],
            model=result["model"],
            usage=result["usage"],
            message="Chat completion successful",
        )

    except OpenAIServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/stream")
async def chat_completion_stream(
    request: ChatRequest, gemini_service: GeminiService = Depends(get_gemini_service)
):
    """Get streaming chat completion"""
    logger.info(f"Received streaming request: {request.message[:100]}...")
    logger.debug(f"Request details: model={request.model}, temp={request.temperature}, max_tokens={request.max_tokens}")
    
    try:

        async def generate_stream() -> AsyncGenerator[str, None]:
            logger.info("Starting generate_stream function")
            chunk_count = 0
            try:
                logger.info("Calling gemini_service.chat_completion_stream...")
                async for chunk in gemini_service.chat_completion_stream(
                    user_message=request.message,
                    conversation_history=request.conversation_history,
                    model=request.model,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                ):
                    chunk_count += 1
                    logger.debug(f"Received chunk #{chunk_count} from Gemini service: {chunk}")
                    
                    # Send Server-Sent Events format with proper SSE structure
                    chunk_data = chunk.model_dump()
                    sse_data = f"id: {chunk_count}\nevent: message\ndata: {json.dumps(chunk_data)}\n\n"
                    logger.debug(f"Sending SSE data: {sse_data[:100]}...")
                    yield sse_data

                    if chunk.is_complete:
                        logger.info(f"Stream completed after {chunk_count} chunks")
                        break

                # Send end signal with proper SSE structure
                logger.info("Sending [DONE] signal")
                yield f"id: {chunk_count + 1}\nevent: done\ndata: [DONE]\n\n"

            except OpenAIServiceException as e:
                logger.error(f"OpenAI service exception in streaming: {e.message}")
                error_data = {
                    "error": {"message": e.message, "status_code": e.status_code}
                }
                yield f"event: error\ndata: {json.dumps(error_data)}\n\n"
            except Exception as e:
                logger.error(f"Unexpected streaming error: {str(e)}", exc_info=True)
                error_data = {
                    "error": {"message": "Streaming failed", "status_code": 500}
                }
                yield f"event: error\ndata: {json.dumps(error_data)}\n\n"

        logger.info("Creating StreamingResponse...")
        response = StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
                "X-Accel-Buffering": "no",
            },
        )
        logger.info("StreamingResponse created successfully")
        return response

    except Exception as e:
        logger.error(f"Stream setup error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to initialize streaming")
