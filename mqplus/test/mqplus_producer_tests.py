import mqplus

producer = mqplus.RabbitProducer("docker.kancy.top", "root", "root123")
producer.putMessage("test", "pika.test.queue")
producer.putMessage("test", "pika2.test.queue")
producer.putMessage("test", "pika3.test.queue")