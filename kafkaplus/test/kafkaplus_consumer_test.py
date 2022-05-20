import kafkaplus

# 接收消息的回调函数
def callback1(data, **kwargs):
    print(data)
    print(kwargs)

consumer = kafkaplus.getConsumer("localhost:9092")
# 监听topic，使用回调函数处理消息
consumer.onListener("test_topic",group="G-test",callback=callback1)