from loguru import logger
import os

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{file.path}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")

logger.remove()  # 先清除默认的 console handler
logger.add(
    log_path,
    rotation="10 MB",
    retention="7 days",
    encoding="utf-8",
    enqueue=True,
    format=LOG_FORMAT,
    level="INFO"
)
logger.add(
    sink=lambda msg: print(msg, end=""),  # 同时输出到控制台
    format=LOG_FORMAT,
    level="INFO"
)