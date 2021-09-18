import logging


logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

logger = logging.getLogger("server")
