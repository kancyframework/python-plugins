### 使用手册

**快速开始**

1) 生产者
```python
import mqplus

producer = mqplus.RabbitProducer("docker.kancy.top", "root", "root123")
producer.putMessage("test", "pika.test.queue")

# 注册交换机
producer.registerExchange("pika.test.exchange", 'direct')

# 注册队列
producer.registerQueue("pika.test.queue", durable=True)

# 绑定交换机很队列
producer.bind("pika.test.exchange", "pika.test.queue")

```

2) 消费者
```python
import mqplus

def handle_message(data, **kwargs):
    print(kwargs)

consumer = mqplus.RabbitConsumer("docker.kancy.top", "root", "root123")
consumer.onListener("pika.test.queue", callback=handle_message)

```