from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class CustomHTTPException(HTTPException):
    """Custom HTTP Exception with additional context"""

    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class GeminiServiceException(Exception):
    """Exception raised by Gemini service operations"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    """Handle custom HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "code": exc.error_code,
                "status_code": exc.status_code,
            }
        },
    )


async def gemini_service_exception_handler(
    request: Request, exc: GeminiServiceException
):
    """Handle Gemini service exceptions"""
    logger.error(f"Gemini service error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "code": "GEMINI_SERVICE_ERROR",
                "status_code": exc.status_code,
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "Internal server error",
                "code": "INTERNAL_ERROR",
                "status_code": 500,
            }
        },
    )
