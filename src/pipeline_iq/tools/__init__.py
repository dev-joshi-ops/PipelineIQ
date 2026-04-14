import httpx
from functools import wraps
from typing import Any, Callable
from loguru import logger
from pipeline_iq.schemas.jenkins import ErrorResponse


def safe_tool(func: Callable) -> Callable:
    """
    Decorator that catches exceptions in MCP tools and returns a structured ErrorResponse.
    This prevents raw stack traces and internal details from leaking to the LLM client.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            if code == 401:
                msg = "CI/CD provider authentication failed. Please check your credentials."
            elif code == 403:
                msg = "Permission denied. The CI/CD user lacks permission for this action."
            elif code == 404:
                msg = "The requested CI/CD resource (job or build) was not found."
            else:
                msg = f"CI/CD provider API error: {code}. Check logs for details."

            logger.error(f"HTTP {code} error in {func.__name__}: {e.response.text}")
            return ErrorResponse(code=f"HTTP_{code}", message=msg)

        except ValueError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            return ErrorResponse(code="VALIDATION_ERROR", message=str(e))

        except Exception:
            logger.exception(f"Unexpected error in {func.__name__}")
            return ErrorResponse(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred while processing the CI/CD request.",
            )

    return wrapper
