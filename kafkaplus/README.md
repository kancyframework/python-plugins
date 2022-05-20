### 使用手册

**快速开始**

1）生产者
```python
import kafkaplus

producer = kafkaplus.getProducer("localhost:9092")
# 发送一条消息
producer.send("test_topic", "data-a")

# 同步发送一条消息
producer.sendSync("test_topic", "data-b")

# 批量发送消息
producer.sendBatch("test_topic", "data1", "data2", "data3")
```

2）消费者
```python
import kafkaplus

# 接收消息的回调函数
def callback(data, **kwargs):
    print(data)
    print(kwargs)

consumer = kafkaplus.getConsumer("localhost:9092")
# 监听topic，使用回调函数处理消息
consumer.onListener("test_topic",group="G-test",callback=callback)
```