### 使用手册

#### 快速开始
```python
import emaileer

# 定义一个QQ Mailer
mailer = emaileer.QQMailer("1727xxxx32@qq.com", "kafnedgxxxxsgjbhg", fromName="姓名")

# 发送文本邮件
mailer.sendText("测试标题", "hello", "7932xxx61@qq.com")

# 发送Html邮件
mailer.sendText("测试标题", "<h3>hello</h3>", "7932xxx61@qq.com")

# 发送Html模板邮件
mailer.sendText("测试标题", "demo.html", "7932xxx61@qq.com", k1='v1', k2='v2')

# 发送附件邮件
mailer.sendText("测试标题", "demo.html", "7932xxx61@qq.com", files="file1.txt,file2.txt")
```