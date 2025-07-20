from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health", summary="Checks if the API is online", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Endpoint to check if the API is online.
    Returns a 200 OK status if the API is working.
    """
    return {"status": "ok", "message": "API is running"}


