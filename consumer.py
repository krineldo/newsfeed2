import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# consumer = KafkaConsumer('my_topic')

all_topics = ["world_cup", "covid", "bitcoin", "war", "nba", "python", "ps5", "f1", "sources_domain_name"]

consumer = KafkaConsumer(*all_topics)

KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('utf-8')))


myclient = MongoClient('localhost', 27017)
mydb = myclient.get_database("newdb")
# mydb = myclient["mydb"]


def process_topic_world_cup(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("world_cup").insert_many(rec)
    print(rec)


def process_topic_covid(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("covid").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_bitcoin(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("bitcoin").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_war(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("war").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_nba(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("nba").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_python(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("python").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_ps5(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("ps5").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_f1(m):
    rec = json.loads(m.value)
    rec = json.dumps(rec["articles"])
    rec = json.loads(rec)
    mydb.get_collection("f1").insert_many(rec)
    print("!!!!!!!!!")


def process_topic_sdn(m):
    rec = json.loads(m.value)
    #rec = json.dumps(rec["articles"])
    print(rec)
    mydb.get_collection("sources").insert_one(rec)
    print("!!!!!!!!!")


func_dict = {"world_cup": process_topic_world_cup,
             "covid": process_topic_covid,
             "bitcoin": process_topic_bitcoin,
             "war": process_topic_war,
             "nba": process_topic_nba,
             "python": process_topic_python,
             "ps5": process_topic_ps5,
             "f1": process_topic_f1,
             "sources_domain_name": process_topic_sdn}

# consumer.subscribe(*all_topics)

for msg in consumer:
    print(msg)
    func_dict[msg.topic](msg)
    print(msg.topic)


