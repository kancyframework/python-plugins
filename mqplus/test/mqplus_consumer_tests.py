import mqplus

def handle_message(data, **kwargs):
    print(kwargs)

consumer = mqplus.getRabbitConsumer("192.168.0.105", "root", "root123")
consumer.onListener("pika.test.queue", callback=handle_message)
consumer.onListener("pika2.test.queue", callback=handle_message)
consumer.onListener("pika3.test.queue", callback=handle_message)