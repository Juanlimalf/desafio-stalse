from logging import Formatter, StreamHandler, getLogger

logger = getLogger()
logger.setLevel("INFO")

handler = StreamHandler()
handler.setFormatter(Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger.addHandler(handler)
