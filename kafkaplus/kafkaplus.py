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



def getProducer(bootstrap_servers,
                username=None,
                password=None,
                encoding='utf-8',
                **configs):
    return SimpleKafkaProducer(bootstrap_servers=bootstrap_servers,
                               username=username,
                               password=password,
                               encoding=encoding,
                               **configs)


def getConsumer(bootstrap_servers,
                username=None,
                password=None,
                encoding='utf-8',
                **configs):
    return SimpleKafkaConsumer(bootstrap_servers=bootstrap_servers,
                               username=username,
                               password=password,
                               encoding=encoding,
                               **configs)

class SimpleKafkaConsumer:
    def __init__(self, bootstrap_servers,
                 username=None,
                 password=None,
                 encoding='utf-8',
                 **configs):
        self.__bootstrap_servers = bootstrap_servers
        self.__username = username
        self.__password = password
        self.__encoding = encoding
        self.__configs = configs
        self.__auth_flag = username and password
        if self.__auth_flag:
            self.__security_protocol = 'SASL_PLAINTEXT'
            self.__sasl_mechanism = 'PLAIN'

    @_async_call
    def onListener(self, topic, group=None, auto_offset_reset='latest',enable_auto_commit=True, callback=None):
        """
        监听消息 (默认只接受新消息)
        :param topic: 主题
        :param group: 消费组，groupId为空时，无法提交offset
        :param auto_offset_reset: 'smallest': 'earliest', 'largest': 'latest'
                    earliest：表示自动重置到 partition 的最小 offset。
                    latest：默认为 latest，表示自动重置到 partition 的最大 offset。
        :param enable_auto_commit: 自动提交
        :param callback: 消息回调函数
        :return:
        """
        assert topic is not None
        assert callback is not None
        import json
        from kafka import KafkaConsumer
        if self.__auth_flag:
            records = KafkaConsumer(topic,bootstrap_servers=self.__bootstrap_servers,
                                 security_protocol=self.__security_protocol,
                                 sasl_mechanism=self.__sasl_mechanism,
                                 sasl_plain_username=self.__username,
                                 sasl_plain_password=self.__password,
                                 group_id=group,
                                 auto_offset_reset=auto_offset_reset,
                                 enable_auto_commit=enable_auto_commit,
                                 value_deserializer=lambda item: json.loads(item.decode(self.__encoding)),
                                 **self.__configs)
        else:
            records = KafkaConsumer(topic,bootstrap_servers=self.__bootstrap_servers,
                                     group_id=group,
                                     auto_offset_reset=auto_offset_reset,
                                     enable_auto_commit=enable_auto_commit,
                                     value_deserializer=lambda item: json.loads(item.decode(self.__encoding)),
                                     **self.__configs)

        print(f"Start listener topic : {topic} on {auto_offset_reset} !")
        for record in records:
            callback(data=record.value, topic=record.topic,partition=record.partition,
                     ts=record.timestamp,timestamp=record.timestamp, msg=record)

class SimpleKafkaProducer:
    def __init__(self,bootstrap_servers,
                 username=None,
                 password=None,
                 encoding='utf-8',
                 **configs):
        import json
        from kafka import KafkaProducer
        if username and password:
            security_protocol = 'SASL_PLAINTEXT'
            sasl_mechanism = 'PLAIN'
            self.__producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       security_protocol=security_protocol,
                                       sasl_mechanism=sasl_mechanism,
                                       sasl_plain_username=username,
                                       sasl_plain_password=password,
                                       value_serializer=lambda v: json.dumps(v).encode(encoding), **configs)
        self.__producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                   value_serializer=lambda v: json.dumps(v).encode(encoding), **configs)


    def sendBatch(self, topic, *datas, partition=None, flush: bool = True, **configs):
        """
        批量发送数据
        :param topic: 消息主题
        :param datas: 数据
        :param partition: 默认轮询机制
        :param configs: 其他配置
        :return:
        """
        for data in datas:
            self.__producer.send(topic=topic, value=data, partition=partition, **configs)
        if flush:
            self.flush()

    def send(self, topic, data, partition=None, flush: bool = True, **configs):
        """
        数据被传入到哪个分区，首先取决于你指定哪个分区，也就是send中partition参数，如果你没有指定partition，
        但是指定了key的话，会根据key的hash而被选中(同一个key会被分配到相同的分区)，如果两者都没有指定，则会按照轮询的方式来分配分区
        """
        assert topic is not None
        assert data is not None
        future = self.__producer.send(topic=topic, value=data, partition=partition, **configs)
        if flush:
            self.flush()
        return future

    def sendSync(self, topic, data, partition=None, timeout: int = 5, **configs):
        """
        数据被传入到哪个分区，首先取决于你指定哪个分区，也就是send中partition参数，如果你没有指定partition，
        但是指定了key的话，会根据key的hash而被选中(同一个key会被分配到相同的分区)，如果两者都没有指定，则会按照轮询的方式来分配分区
        """
        assert topic is not None
        assert data is not None
        import kafka
        try:
            future = self.__producer.send(topic=topic, value=data, partition=partition, **configs)
            return future.get(timeout=timeout)
        except kafka.errors.kafka_errors:
            return None

    def flush(self):
        return self.__producer.flush()

    def close(self):
        return self.__producer.close()
