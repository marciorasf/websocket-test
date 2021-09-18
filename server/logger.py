import logging


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

logger = logging.getLogger("server")
