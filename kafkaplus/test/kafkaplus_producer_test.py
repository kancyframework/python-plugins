import kafkaplus

producer = kafkaplus.getProducer("localhost:9092")
# 发送一条消息
producer.send("test_topic", "data-a")

# 同步发送一条消息
producer.sendSync("test_topic", "data-b")

# 批量发送消息
producer.sendBatch("test_topic", "data1", "data2", "data3")