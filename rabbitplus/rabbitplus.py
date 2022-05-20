def _async_call(fn):
    """
    内部异步调用
    :param fn:
    :return:
    """
    import threading

    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class RabbitConsumer:
    """
    RabbitMQ Simple Consumer
    """

    def __init__(self, host: str, username: str, password: str, port: int = 5672, virtual_host: str = '/', **kwargs):
        self.password = password
        self.username = username
        self.port = port
        self.host = host
        self.virtual_host = virtual_host
        self.props = kwargs

    def __get_conn(self):
        import pika
        return pika.BlockingConnection(
            pika.ConnectionParameters(virtual_host=self.virtual_host, host=self.host, port=self.port,
                                      credentials=pika.PlainCredentials(self.username, self.password), **self.props))

    def registerQueue(self, queue: str, durable: bool = True):
        """
        绑定队列
        :param queue:
        :param durable:
        :return:
        """
        if queue:
            mq_conn = self.__get_conn()
            mq_channel = mq_conn.channel()
            mq_channel.queue_declare(queue=queue, durable=durable)
            mq_channel.close()
            mq_conn.close()

    def registerExchange(self, exchange: str, exchange_type: str = 'direct', durable: bool = True):
        """
        绑定/申明交换机
        :param exchange:交换机名称
        :param exchange_type: 'direct','fanout','headers','topic'
        :param durable:支持化
        :return:
        """
        if exchange:
            assert exchange_type in ['direct', 'fanout', 'headers', 'topic']
            mq_conn = self.__get_conn()
            mq_channel = mq_conn.channel()
            mq_channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=durable)
            mq_channel.close()
            mq_conn.close()

    def bind(self, exchange: str, queue: str, routing_key=None, arguments=None):
        """
        绑定队列和交换机
        :param exchange:交换机
        :param queue:队列
        :param routing_key: 路由key
        :param arguments:key、value
        :return:
        """
        if exchange and queue:
            mq_conn = self.__get_conn()
            mq_channel = mq_conn.channel()
            mq_channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key, arguments=arguments)
            mq_channel.close()
            mq_conn.close()

    @_async_call
    def onListener(self, queue: str, callback, auto_ack: bool = False, prefetch_count: int = 10, durable: bool = True,
                   **kwargs):
        """
        :param queue: 队列名
        :param callback: 回调的函数对象
        :param auto_ack: 自动ack
        :param durable: 队列不存在时创建队列，持久化
        :param prefetch_count: 预取消息数量
        :return:
        """
        assert queue is not None

        import pika
        def __on_message_callback(channel: pika.adapters.blocking_connection.BlockingChannel,
                                  deliver: pika.spec.Basic.Deliver,
                                  props: pika.spec.BasicProperties, message):

            print(
                f"Consumer({deliver.consumer_tag})接收到[exchange={deliver.exchange}|queue={deliver.routing_key}|tag={deliver.delivery_tag}]的消息：{message}")

            if auto_ack:
                return callback(message, props=props, deliver=deliver, channel=channel)
            try:
                callback(message, props=props, deliver=deliver, channel=channel)
            except Exception:
                channel.basic_nack(delivery_tag=deliver.delivery_tag)
                raise
            else:
                channel.basic_ack(delivery_tag=deliver.delivery_tag)

        mq_conn = self.__get_conn()
        mq_channel = mq_conn.channel()
        mq_channel.basic_qos(prefetch_count=prefetch_count)
        # 消费者创建队列，生产者创建交换机
        mq_channel.queue_declare(queue, durable=durable, **kwargs)
        mq_channel.basic_consume(
            on_message_callback=__on_message_callback,
            queue=queue,
            auto_ack=auto_ack,
            **kwargs
        )
        # 开始接收(将数据放入回调函数开始执行)
        print(f"Start listener queue : {queue} , ack = {auto_ack} !")
        mq_channel.start_consuming()
        # 关闭资源
        mq_channel.close()
        mq_conn.close()


class RabbitProducer:
    """
    RabbitMQ Simple Producer
    """

    def __init__(self, host: str, username: str, password: str, port: int = 5672, virtual_host: str = '/',
                 prefetch_count: int = 10,
                 **kwargs) -> None:
        self.__prefetch_count = prefetch_count

        # 获取与rabbitmq 服务的连接
        import pika
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(virtual_host=virtual_host, host=host, port=port,
                                      credentials=pika.PlainCredentials(username, password)), **kwargs)
        self.__channel = self.__init_channel()

    def __init_channel(self):
        mq_channel = self.__connection.channel()
        # prefetch_count: 通道的最大容量
        mq_channel.basic_qos(prefetch_count=self.__prefetch_count)
        return mq_channel

    def _get_channel(self):
        if self.__channel:
            return self.__channel
        else:
            self.__channel = self.__init_channel()
            return self.__channel

    def close(self):
        """
        关闭资源
        :return:
        """
        if self.__channel:
            self.__channel.close()
        if self.__connection:
            self.__connection.close()

    def registerQueue(self, queue: str, durable: bool = True):
        """
        绑定队列
        :param queue:
        :param durable:
        :return:
        """
        if queue:
            mq_channel = self._get_channel()
            mq_channel.queue_declare(queue=queue, durable=durable)

    def registerExchange(self, exchange: str, exchange_type: str = 'direct', durable: bool = True):
        """
        绑定/申明交换机
        :param exchange:交换机名称
        :param exchange_type: 'direct','fanout','headers','topic'
        :param durable:支持化
        :return:
        """
        if exchange:
            assert exchange_type in ['direct', 'fanout', 'headers', 'topic']
            mq_channel = self._get_channel()
            mq_channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=durable)

    def bind(self, exchange: str, queue: str, routing_key='#', arguments=None):
        """
        绑定队列和交换机
        :param exchange:交换机
        :param queue:队列
        :param routing_key:路由key
        :param arguments:key、value
        :return:
        """
        if exchange and queue and len(exchange) > 0:
            mq_channel = self._get_channel()
            mq_channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key, arguments=arguments)


    def send(self, message, exchange: str = None, routing_key: str = '#',
             delivery_mode: int = 2,
             mandatory: bool = False,
             **kwargs):
        """
        发送消息
        """
        if exchange is None:
            exchange = ''
            assert routing_key is not None

        import pika
        mq_channel = self._get_channel()
        return mq_channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=delivery_mode, **kwargs),
            mandatory=mandatory
        )

    def sendExchange(self, message, exchange, routing_key: str = '#', **kwargs):
        """
        发送消息
        """
        assert message is not None
        assert exchange is not None
        return self.send(message=message, exchange=exchange, routing_key=routing_key, **kwargs)

    def sendQueue(self, message, queue, **kwargs):
        """
        发送消息
        """
        assert message is not None
        assert queue is not None
        return self.send(message=message, routing_key=queue, **kwargs)

    def putExchange(self, message, exchange, routing_key: str = '#', **kwargs):
        """
        发送消息
        """
        assert message is not None
        assert exchange is not None
        return self.send(message=message, exchange=exchange, routing_key=routing_key, **kwargs)

    def putQueue(self, message, queue, **kwargs):
        """
        发送消息
        """
        assert message is not None
        assert queue is not None
        return self.send(message=message, routing_key=queue, **kwargs)
