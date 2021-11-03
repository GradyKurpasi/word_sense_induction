from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback


# endpoint = 'wss://word-knowledge-db.gremlin.cosmosdb.azure.com:443/'
ENDPOINT = 'wss://word-knowledge-db.gremlin.cosmos.azure.com:443/'
KEY = 'nioOwS9IVVs1kEsXhQ65lfSP5jD5ZKRIOAQYUpAIC3I2ZsZvZo5AFfZtJkgtrW0zhTn6uEPGTNSRDYwZXcCxUg=='
USERNAME = '/dbs/WordKnowledge/colls/WordSense'



def connect_cosmosdb_client(connect_string=ENDPOINT, user=USERNAME, passw=KEY):
    dbclient =  client.Client(
                        connect_string, 
                        'g',
                        username=user,
                        password=passw,
                        message_serializer=serializer.GraphSONSerializersV2d0()
                        )
    return dbclient




# def insert_vertices(client):
#     for query in _gremlin_insert_vertices:
#         print("\n> {0}\n".format(query))
#         callback = client.submitAsync(query)
#         if callback.result() is not None:
#             print("\tInserted this vertex:\n\t{0}".format(
#                 callback.result().all().result()))
#         else:
#             print("Something went wrong with this query: {0}".format(query))
#         print("\n")
#         print_status_attributes(callback.result())
#         print("\n")
#     print("\n")



# insert_vertices(dbclient)