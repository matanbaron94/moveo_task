from confluent_kafka import Consumer,Producer
from src.local_config import config
from threading import Thread



####################################################
###################### INIT ########################
####################################################

PRODUCER_CONFIG = {'bootstrap.servers':f'{config["KAFKA_HOST_NAME"]}:{config["KAFKA_PORT"]}'}
CONCUMER_CONFIG = {
                    'bootstrap.servers':f'{config["KAFKA_HOST_NAME"]}:{config["KAFKA_PORT"]}',
                    'group.id': 'ms_inventory',
                    'auto.offset.reset': 'earliest'
                   }



####################################################
##################### PRODUCER #####################
####################################################

class kafkaProducer():

    def __init__(self, topics):

        self.__kafka_driver__ = Producer(PRODUCER_CONFIG)
        for topic in topics:
            self.send_msg(topic,"init msg")


    def send_msg(self, topic, msg):
        self.__kafka_driver__.produce(
                   topic,
                    value=str(msg),
                    
                    )
        self.__kafka_driver__.flush()
        print("Message sent!")



####################################################
##################### CONSUMER #####################
####################################################

class kafkaConsumer():
    def __init__(self,topics_to_subscribe:list):

        self.__kafka_driver__ = Consumer(CONCUMER_CONFIG)
        self.__kafka_driver__.subscribe(topics_to_subscribe)


    def __get_msgs__(self):

        while True:
            msg = self.__kafka_driver__.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            print(f"Received message: \nTocic: {msg.topic()}\nMessage: {msg.value().decode('utf-8')}")
            
    
    
    def get_msgs(self):
        t = Thread(target=self.__get_msgs__, args=[])
        t.start()
