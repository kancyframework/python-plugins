
**使用教程**
```python
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
logger = log.Logger(color=True, tag="demo", file="test_{date}.log")
logger.debug("debug log")
logger.info("info log")
logger.warn("warn log")
logger.error("error log")
logger.success("success log")
logger.log("good log", "GOOD")
```

1）文字效果
```text
2021-11-27 01:17:56.316447 DEBUG 115872 <mainthread> - [log_tests.py::6] : debug log
2021-11-27 01:17:56.316447  INFO 115872 <mainthread> - [log_tests.py::7] : info log
2021-11-27 01:17:56.316447  WARN 115872 <mainthread> - [log_tests.py::8] : warn log
2021-11-27 01:17:56.316447 ERROR 115872 <mainthread> - [log_tests.py::9] : error log
2021-11-27 01:17:56.316447    OK 115872 <mainthread> - [log_tests.py::10] : success log
2021-11-27 01:17:56.316447  GOOD 115872 <mainthread> - [log_tests.py::11] : good log
2021-11-27 01:17:56.316447 DEBUG 115872 <mainthread> - [log_tests.py::16] (demo) : debug log
2021-11-27 01:17:56.316447  INFO 115872 <mainthread> - [log_tests.py::17] (demo) : info log
2021-11-27 01:17:56.316447  WARN 115872 <mainthread> - [log_tests.py::18] (demo) : warn log
2021-11-27 01:17:56.316447 ERROR 115872 <mainthread> - [log_tests.py::19] (demo) : error log
2021-11-27 01:17:56.316447    OK 115872 <mainthread> - [log_tests.py::20] (demo) : success log
2021-11-27 01:17:56.316447  GOOD 115872 <mainthread> - [log_tests.py::21] (demo) : good log
```

2）图片效果

![img.png](https://images.cnblogs.com/cnblogs_com/kancy/2069805/o_211126152754_img.png)
