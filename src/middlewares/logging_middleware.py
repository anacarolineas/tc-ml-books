import time
from fastapi import Request
import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
log = structlog.get_logger()

async def structured_logging_middleware(request: Request, call_next):
    start_time = time.time()

    client_host = request.client.host if request.client else None

    log.info(
        "request_started", 
        method=request.method, 
        path=request.url.path,
        client_host=client_host
    )

    try:
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        
        log.info(
            "request_finished",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time, 2)
        )
        
        return response
        
    except Exception as exc:
        process_time = (time.time() - start_time) * 1000
        
        log.error(
            "request_error",
            method=request.method,
            path=request.url.path,
            client_host=client_host,
            error=str(exc),
            error_type=type(exc).__name__,
            process_time_ms=round(process_time, 2)
        )
        raise