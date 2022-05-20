### 使用手册

**快速开始**

1) 生产者
```python
import rabbitplus

producer = rabbitplus.RabbitProducer("docker.kancy.top", "root", "root123")
producer.putQueue("test", "pika.test.queue")

# 注册交换机
producer.registerExchange("pika.test.exchange", 'direct')

# 注册队列
producer.registerQueue("pika.test.queue", durable=True)

# 绑定交换机很队列
producer.bind("pika.test.exchange", "pika.test.queue")

```

2) 消费者
```python
import rabbitplus

def handle_message(data, **kwargs):
    print(kwargs)

consumer = rabbitplus.RabbitConsumer("docker.kancy.top", "root", "root123")
consumer.onListener("pika.test.queue", callback=handle_message)

```