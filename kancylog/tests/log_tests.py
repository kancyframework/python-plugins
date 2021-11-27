import kancylog as log

# 控制是否打印彩色日志，默认是True
# log.disablePrintColor()

# 使用默认的Logger实例
log.debug("debug log")
log.info("info log")
log.warn("warn log")
log.error("error log")
log.success("success log")
log.log("good log", "GOOD")


# 自定义Logger对象
logger = log.Logger(color=True, tag="demo", file="{desktop}\\data\\test_{time}.log")
logger.debug("debug log")
logger.info("info log")
logger.warn("warn log")
logger.error("error log")
logger.success("success log")
logger.log("good log", "GOOD")
