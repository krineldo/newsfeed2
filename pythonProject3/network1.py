from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import pandas as pd


def MongoDB():
    myclient = MongoClient('localhost', 27017)
    mydb = myclient["newdb"]
    return mydb


client = MongoDB()

wc_g = nx.Graph()


keys = ["world_cup"]
# ,"covid", "bitcoin", "war", "nba", "python", "ps5", "f1"
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


for d in dicts:
    wc_g.add_node(d['_id'], attr_dict=d)


#failed attempt
# def colls(keywords):
#     dicts = [d for d in coll.find()]
#     return dicts
#
#
# # dicts = []
# for k in keys:
#     coll = client[k]
#     dicts = colls(k)
#



#ayto douleuei
# world_cup = client["world_cup"]
# dicts = [d for d in world_cup.find()]
#
# world_cup = client["world_cup"]
# dicts = [d for d in world_cup.find()]


# wc_g = nx.Graph()
# for d in dicts:
#     wc_g.add_node(d['_id'], attr_dict=d)

#attempt 1 :very slow but correct possibly

# for d in dicts:
#     for d2 in dicts:
#         if d['_id'] != d2['_id']:
#             if d['source'] == d2['source'] or d['author'] == d2['author']:
#                 wc_g.add_edge(d['_id'], d2['_id'])
#             else:
#                 closest_node = None
#                 closest_time = None
#                 for d3 in dicts:
#                     if d3['_id'] != d['_id'] and d3['_id'] != d2['_id']:
#                         time_diff = abs(datetime.datetime.strptime(d['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') - datetime.datetime.strptime(d3['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'))
#                         if closest_node is None or time_diff < closest_time:
#                             closest_node = d3['_id']
#                             closest_time = time_diff
#                 if closest_node is not None:
#                     wc_g.add_edge(d['_id'], closest_node)




# #attempt 3 fast way
# Create empty graph

# Add nodes to graph
# Add edges to graph
for i in range(len(dicts)):
    for j in range(i+1, len(dicts)):
        if dicts[i]['source'] == dicts[j]['source'] or dicts[i]['author'] == dicts[j]['author']:
            wc_g.add_edge(dicts[i]['_id'], dicts[j]['_id'])
        # Στην περίπτωση που για έναν κόμβο δεν ισχύει ούτε το (α.) ούτε το
        # (β.) τότε συνδέεται με τον κόμβο που έχει το πιο κοντινό timestamp.
        # uncomment εδω για το 3ο condition. Εμείς δεν το τρεχουμε
        # για να μην μας παρει πολυ ωρα

        # else:
        #     closest_node = None
        #     closest_time = None
        #     for k in range(len(dicts)):
        #         if k != i and k != j:
        #             timestamp1 = dicts[i]['publishedAt']
        #             timestamp2 = dicts[k]['publishedAt']
        #             time_diff = abs(
        #                 datetime.datetime.strptime(timestamp1, '%Y-%m-%dT%H:%M:%SZ') - datetime.datetime.strptime(
        #                     timestamp2, '%Y-%m-%dT%H:%M:%SZ'))
        #             if closest_node is None or time_diff < closest_time:
        #                 closest_node = dicts[k]['_id']
        #                 closest_time = time_diff
        #     if closest_node is not None:
        #         wc_g.add_edge(dicts[i]['_id'], closest_node)

print("mpika")
print(wc_g.number_of_nodes())
print(wc_g.number_of_edges())

# for n in wc_g:
#     wc_g.node[n]['id'] = wc_g.node[n]['_id']
#     del wc_g.node[n]['_id']


nx.write_gexf(wc_g, "graph")
new_nx = nx.read_gexf("graph")

neighbors = new_nx.neighbors("63b594b5d224184ca7f52b2c")
nums = []
for n in new_nx.neighbors("63b594b5d224184ca7f52b2c"):
    nums.append(new_nx.degree[n])

print(max(nums))

max_degree_neighbor = max(neighbors, key=lambda x: new_nx.degree[x])
print(max_degree_neighbor)
print(new_nx.degree(max_degree_neighbor))





# pos = nx.spring_layout(wc_g)
#
# # Draw the edges in blue
# nx.draw_networkx_edges(wc_g, pos, edge_color='blue')
#
# # Draw the nodes in red
# nx.draw_networkx_nodes(wc_g, pos, node_color='red', node_size=20)
#
# # Add labels to the nodes
# # nx.draw_networkx_labels(wc_g, pos, font_size=16, font_family='sans-serif')
#
# # Add a title to the graph
# plt.title("My Directed Graph", fontsize=20)
#
# # Remove the axis from the plot
# plt.axis('off')
#
#
#
# # nx.draw(wc_g, with_labels=True)
# # nx.draw_networkx(wc_g)
# # nx.draw_networkx_edges(wc_g)
# plt.show()