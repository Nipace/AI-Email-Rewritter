from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.models.email import EmailRewriteRequest, EmailRewriteResponse
from app.services.email_service import EmailRewriteService


router = APIRouter(prefix="/api", tags=["Email Rewriter"])

email_service = EmailRewriteService()


@router.post(
    "/rewrite",
    response_model=EmailRewriteResponse,
    status_code=status.HTTP_200_OK,
)
async def rewrite_email(
    request: EmailRewriteRequest,
) -> EmailRewriteResponse:
    try:
        rewritten_email = email_service.rewrite_email(request)

        return EmailRewriteResponse(
            rewritten_email=rewritten_email,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to rewrite the email. Please try again.",
        ) from error
@router.post("/rewrite/stream")
async def stream_rewrite_email(
    request: EmailRewriteRequest,
) -> StreamingResponse:
    try:
        return StreamingResponse(
            email_service.stream_rewrite_email(request),
            media_type="text/plain",
            headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
            },
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to rewrite the email. Please try again.",
        ) from error