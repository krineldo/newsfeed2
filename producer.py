import json
import time
import msgpack as msgpack
#import schedule as schedule
import requests
from kafka import KafkaProducer
from newsapi import NewsApiClient
from kafka.errors import KafkaError

tpcs = ["world_cup", "covid", "bitcoin", "war", "nba", "python", "ps5", "f1"]

# producer = KafkaProducer()
# print(producer.bootstrap_connected())
# producer.send('my_topic', b'Hello world').get(timeout=30)

producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'))
producer.send('json-topic', {'key': 'value'})

newsapi = NewsApiClient(api_key='123872d2ae724bdcabbcfec16dc712d8')
#123872d2ae724bdcabbcfec16dc712d8 my key
#a734b986e6664b10b4b74666cfc77bfe paulos key
#e427ea4438ed46fc9e6d0df36478a646 3d api key

# all_articles = newsapi.get_everything(q='world_cup', from_param='2022-11-29')

# print(all_articles)


# def api_calls():
#     for x in tpcs:
#         all_articles = newsapi.get_everything(q=x, from_param='2022-11-29')
#         producer.send(x, all_articles)
#         sources = newsapi.get_sources()
#         media_wiki_call(sources)
#         print(all_articles)
#
#
# # schedule.every(2).hours.do(api_calls())
# schedule.every(1).minutes.do(api_calls)
#
# while True:
#     schedule.run_pending()
# #     time.sleep(1)

data_dict = {}

def media_wiki_call(subject):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {'action': 'query', 'format': 'json', 'titles': subject, 'prop': 'extracts', 'exintro': True,
              'explaintext': True}

    response = requests.get(url, params=params)
    data = response.json()
    # print(data)
    data = data['query']
    data = data['pages']
    # if data['-1']:
    # print(data)
    if data.get('-1') == None:
        print(data)
        for key in data:
            print(data.get(key))
            # data_dict[key] = data.get(key)
            # data_dict["title"] = data.get(key)
            tr = {"title": data.get(key)}
            source_send(tr)
        #
    # source_send(data_dict)
    # if '-1' in data:
    # print(data.keys())
    # if missing doesn't exist do
    # return data_dict


def source_send(diction):
    print(diction)
    print(diction.keys())
    producer.send("sources_domain_name", diction)


while 1==1:
    for x in tpcs:
        all_articles = newsapi.get_everything(q=x, from_param='2022-12-12', language='en', sort_by='relevancy')
        producer.send(x, all_articles)
        #sources = newsapi.get_sources()
        print(type(all_articles))
        articles = all_articles.get('articles')
        #articles = json.dumps(articles)
        #print(articles.get('source'))
        sources = [l['source'] for l in articles]
        names = [l['name'] for l in sources]
        print(names)
        for n in names:
            media_wiki_call(n)
        # source_send(data_dict)

    time.sleep(40)




