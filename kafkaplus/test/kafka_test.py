from kafka import KafkaProducer
import randomer

# 创建生产者
producer = KafkaProducer(bootstrap_servers='localhost:9092')
for i in range(0,20):
    msg = f'哈哈{randomer.randomUuid()}'.encode('utf-8')  # 发送内容,必须是bytes类型
    # 可以通过send方法中的partition参数指定分区传入
    producer.send('test', msg)
producer.close()