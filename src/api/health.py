
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health", summary="Verifica se a API está no ar", status_code=status.HTTP_200_OK,)
async def liveness_check():
    """
    Endpoint para verificar se a API está no ar.
    Retorna um status 200 OK se a API estiver funcionando.
    """
    return {"status": "ok", "message": "API is running"}


