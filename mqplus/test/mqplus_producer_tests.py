import mqplus

producer = mqplus.getRabbitProducer("192.168.0.105", "root", "root123")
producer.putQueue("test", "pika.test.queue")
producer.putQueue("test", "pika2.test.queue")
producer.putQueue("test", "pika3.test.queue")