def getRabbitConsumer(host: str, username: str, password: str, port: int = 5672, virtual_host: str = '/', **configs):
    import rabbitplus
    return rabbitplus.RabbitConsumer(
        host=host, username=username, password=password, port=port, virtual_host=virtual_host, **configs)


def getRabbitProducer(host: str, username: str, password: str, port: int = 5672, virtual_host: str = '/', **configs):
    import rabbitplus
    return rabbitplus.RabbitProducer(
        host=host, username=username, password=password, port=port, virtual_host=virtual_host, **configs)


def getKafkaProducer(bootstrap_servers,username=None,password=None,encoding='utf-8',**configs):
    import kafkaplus
    return kafkaplus.getProducer(
        bootstrap_servers=bootstrap_servers, username=username, password=password, encoding=encoding,**configs)


def getKafkaConsumer(bootstrap_servers,username=None,password=None,encoding='utf-8',**configs):
    import kafkaplus
    return kafkaplus.getConsumer(
        bootstrap_servers=bootstrap_servers, username=username, password=password, encoding=encoding,**configs)