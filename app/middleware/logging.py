# app/middlewares/logging.py
import os
import time
import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request
from fastapi.responses import Response

# --------------------------
# Crear carpeta logs si no existe
# --------------------------
os.makedirs("logs", exist_ok=True)

# --------------------------
# Configuración del logger
# --------------------------
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Handler consola (todos los logs)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_formatter)

# Handler archivo (solo errores) con rotación
file_handler = RotatingFileHandler(
    "logs/errors.log",      # dentro de carpeta logs/
    maxBytes=1_000_000,     # 1 MB por archivo
    backupCount=5           # mantener 5 archivos antiguos
)
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Agregar handlers al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# --------------------------
# Middleware de logging
# --------------------------
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    try:
        response: Response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        # Registrar excepción
        status_code = 500
        logger.error(
            f"EXCEPTION - {request.method} {request.url.path} "
            f"- User: {getattr(request.state, 'user_id', 'anon')} "
            f"- IP: {request.client.host} "
            f"- {str(e)}"
        )
        raise e

    duration = time.time() - start_time
    user = getattr(request.state, "user_id", "anon")
    ip = request.client.host

    log_message = (
        f"User: {user} - IP: {ip} - {request.method} {request.url.path} "
        f"- Status: {status_code} - {duration:.3f}s"
    )

    # INFO para requests exitosas
    if status_code < 400:
        logger.info(log_message)
    # WARNING para errores cliente
    elif status_code < 500:
        logger.warning(log_message)
    # ERROR para errores servidor
    else:
        logger.error(log_message)

    return response