from pymongo import MongoClient

tpcs = ["world_cup", "covid", "bitcoin", "war", "nba", "python", "ps5", "f1"]

client = MongoClient('mongodb://localhost:27017/')

db = client['newdb']
print("Database created........")


for x in tpcs:
    myTemplate = "{} = \"{}\""
    statement = myTemplate.format(x, x)
    exec(statement)
    x = db[x]

sources = db['sources']
users = db['users']

for coll in db.list_collection_names():
    print(coll)
