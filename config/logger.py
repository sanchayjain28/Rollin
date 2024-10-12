from loguru import logger

logger.add(sink='logs/rollin.log',
        enqueue=True,
        rotation='1 week',
        colorize=True, 
        format="{time} {level} {message}", 
        level="INFO")