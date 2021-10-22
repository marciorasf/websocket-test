import logging

import coloredlogs

coloredlogs.install(level=logging.INFO)
logger = logging.getLogger("server")

logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
