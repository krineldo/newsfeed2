from pymongo import MongoClient
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import Counter



def MongoDB():
    myclient = MongoClient('localhost', 27017)
    mydb = myclient["newdb"]
    return mydb


client = MongoDB()


# dicts calculations

world_cup = client["world_cup"]
dicts = [d for d in world_cup.find()]
covid = client["covid"]
dicts.extend([d for d in covid.find()])
# dicts_c = [d for d in covid.find()]
bitcoin = client["bitcoin"]
dicts.extend([d for d in bitcoin.find()])
war = client["war"]
dicts.extend([d for d in war.find()])
nba = client["nba"]
dicts.extend([d for d in nba.find()])
python = client["python"]
dicts.extend([d for d in python.find()])
ps5 = client["ps5"]
dicts.extend([d for d in ps5.find()])
f1 = client["f1"]
dicts.extend([d for d in f1.find()])

max_published_at = max(
    datetime.strptime(document["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
    for document in dicts
)

print(max_published_at)
days5_ago = max_published_at - timedelta(days=5)
print(days5_ago)


#end of dicts calculations

wc_dicts = [d for d in world_cup.find()]
covid_dicts = [d for d in covid.find()]
bitcoin_dicts = [d for d in bitcoin.find()]
war_dicts = [d for d in war.find()]
nba_dicts = [d for d in nba.find()]
python_dicts = [d for d in python.find()]
ps5_dicts = [d for d in ps5.find()]
f1_dicts = [d for d in f1.find()]

ds = [wc_dicts, covid_dicts, bitcoin_dicts, war_dicts, nba_dicts, python_dicts, ps5_dicts, f1_dicts]

max_published_at = max(
    datetime.strptime(document["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
    for document in dicts
)


latest_date = max(datetime.strptime(d['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') for d in dicts)

# Define the range of dates to count the articles for
date_range = [latest_date - timedelta(days=i) for i in range(5)]
for d in date_range:
    print(d)
# Initialize a dictionary to count the articles for each collection in the specific date
counts = Counter()
# Loop through the articles and count the number of articles for each collection in the specific date
for dic in ds:
    for article in dic:
        article_date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date()
        print(article_date)
        for d in date_range:
            if article_date == d.date():
                counts[article['_id']] += 1
        # if article_date in [d.date() for d in date_range]:
        #     print(article_date)
        #     counts[article['_id']] += 1
    print(len(counts))

# The count of articles for each collection in the specific date
#print(len(counts))


# tpcs = ["world_cup":world_cup, "covid", "bitcoin", "war", "nba", "python", "ps5", "f1"]

# w_c = client["world_cup"]
#
# for ac in w_c.find().sort("publishedAt"):
#     print(ac)

# x = ['1', '2', '3', '4', '5']
#
# plt.xlabel("Days")
# plt.ylabel("Topics")
# plt.legend(["world_cup", "covid", "bitcoin", "war", "nba", "python", "ps5", "f1"])
# plt.title("Published articles of last 5 days")



