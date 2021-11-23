### 使用手册

**1.快速开始**

1）配置全局配置

默认搜索路径：`emaileer.ini`、`emailer.ini`、`~/emaileer.ini`、`~/emailer.ini`

```ini
[demo-sender]
host = smtp.qq.com
port = 25
username = 172xxx032@qq.com
password = kafnxxxxtjsgjbhg

[test-sender]
host = smtp.qq.com
port = 25
username = 1727xxxx032@qq.com
password = kafnxxxxtjsgjbhg
fromName = kancy
encoding = utf-8
debug = True
```

2）使用指定email sender发送邮件

```python
import emaileer

# 发送文本邮件
emaileer.sendText("demo-sender", "测试标题", "hello", "7932xxx61@qq.com")

# 发送Html邮件
emaileer.sendText("demo-sender", "测试标题", "<h3>hello</h3>", "7932xxx61@qq.com")

# 发送Html模板邮件
emaileer.sendText("test-sender", "测试标题", "demo.html", "7932xxx61@qq.com", k1='v1', k2='v2')

# 发送附件邮件
emaileer.sendText("test-sender", "测试标题", "demo.html", "7932xxx61@qq.com", files="file1.txt,file2.txt")
```

**2.使用内置EmailSender**

- QQ邮箱:`QQEmailSender`
- 网易邮箱:`NeteaseEmailSender`
- 谷歌邮箱:`GoogleEmailSender`

```python
import emaileer

# 定义一个QQ Email Sender
sender = emaileer.QQEmailSender("1727xxxx32@qq.com", "kafnedgxxxxsgjbhg", fromName="姓名")

# 发送文本邮件
sender.sendText("测试标题", "hello", "7932xxx61@qq.com")

# 发送Html邮件
sender.sendText("测试标题", "<h3>hello</h3>", "7932xxx61@qq.com")

# 发送Html模板邮件
sender.sendText("测试标题", "demo.html", "7932xxx61@qq.com", k1='v1', k2='v2')

# 发送附件邮件
sender.sendText("测试标题", "demo.html", "7932xxx61@qq.com", files="file1.txt,file2.txt")
```

**3.自定义EmailSender**

```python
import emaileer

# 自定义
sender = emaileer.EmailSender("smtp.qq.com", 443, "username", "password")
# 发送文本邮件
sender.sendText("测试标题", "hello", "7932xxx61@qq.com")
```