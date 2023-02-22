from pymongo import MongoClient
from datetime import datetime, timedelta
# from collections import defaultdict, Counter
import matplotlib.pyplot as plt
# from collections import Counter
import numpy as np



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

# print(max_published_at)
days5_ago = max_published_at - timedelta(days=5)
# print(days5_ago)

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
# for d in date_range:
    #print(d)

arr = [[0 for i in range(5)] for j in range(8)]
print(arr)
j = 0

for dic in ds:
    i = 0

    for d in date_range:
        i += 1
    j += 1
print(i)
print(j)
j = 0
i = 0
for dic in ds:
    i = 0
    for d in date_range:
        for article in dic:
            article_date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date()

            if article_date == d.date():
                arr[j][i] += 1
                #print(article_date)
        i += 1
    j += 1
print(i)
print(j)


# for date in date_range:
#     print(f"Date: {date}")
#     print(counts[date])
#     print()
print(arr)

# tpcs = ["world_cup":world_cup, "covid", "bitcoin", "war", "nba", "python", "ps5", "f1"]

# w_c = client["world_cup"]
#
# for ac in w_c.find().sort("publishedAt"):
#     print(ac)

x = ['1', '2', '3', '4', '5']
n = 0


    # for el in arr[n][0]:
y1 = np.array(arr[0])

y2 = np.array(arr[1])
y3 = np.array(arr[2])
y4 = np.array(arr[3])
y5 = np.array(arr[4])
y6 = np.array(arr[5])
y7 = np.array(arr[6])
y8 = np.array(arr[7])


print(y1)
plt.bar(x, y1, color='r')
plt.bar(x, y2, bottom=y1, color='b')
plt.bar(x, y3, bottom=y1+y2, color='y')
plt.bar(x, y4, bottom=y1+y2+y3, color='g')
plt.bar(x, y5, bottom=y1+y2+y3+y4, color='m')
plt.bar(x, y6, bottom=y1+y2+y3+y4+y5, color='k')
plt.bar(x, y7, bottom=y1+y2+y3+y4+y5+y6, color='grey')
plt.bar(x, y8, bottom=y1+y2+y3+y4+y5+y6+y7, color='c')

# fig, ax = plt.subplots()
# for i in range(arr.shape[1]):
#     if i == 0:
#         ax.bar(range(arr.shape[0]), arr[:, i], label=f'Column {i}')
#     else:
#         ax.bar(range(arr.shape[0]), arr[:, i], bottom=np.sum(arr[:, :i], axis=1), label=f'Column {i}')

plt.xlabel("Days")
plt.ylabel("Topics")
plt.legend(["world_cup", "covid", "bitcoin", "war", "nba", "python", "ps5", "f1"])
plt.title("Published articles of last 5 days")
plt.savefig('plot.png')


