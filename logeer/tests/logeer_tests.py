import logeer as log

# 日志输出到文件
log.addLogFile("test")

# 日志级别
log.trace("trace log")
log.logger.info("info log")
log.warn("warn log")
log.debug("debug log")
log.error("error log")
log.success("success log")

# 捕获异常
@log.catch
def raise_error():
    raise RuntimeError("run error")

raise_error()
log.success("我可以被执行，不会阻塞！")
raise_error()