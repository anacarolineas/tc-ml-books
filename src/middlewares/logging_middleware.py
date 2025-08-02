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

    log.info(
        "request_started", 
        method=request.method, 
        path=request.url.path,
        client_host=request.client.host
    )

    process_time = (time.time() - start_time) * 1000

    try:
        response = await call_next(request)
    except Exception as exc:
        log.error(
            "request_error",
            method=request.method,
            path=request.url.path,
            client_host=request.client.host,
            error=str(exc),
            process_time_ms=round(process_time, 2)
        )
        raise

    log.info(
        "request_finished",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time_ms=round(process_time, 2)
    )

    return response