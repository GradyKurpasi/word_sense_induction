from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
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

    # # Synchronous Query Submit
    # query = "g.addV('person').property('id', 'Crusty').property('pk', '/pk')"
    # result_set = dbclient.submit(query)   # returns a ResultSet, blocks until request written to Server
    # future_results = result_set.all()     # .all() returns a Future that resolves to a list when Server processing complete
    # results = future_results.result()     # blocks until response received from Server
    # if result_set is None:
    #     raise Exception("CosmosDB Error: {}".format(query))
    # print(results)

    # # ASynchronous Query Submit
    # query = "g.addV('person').property('id', 'Homie').property('pk', '/pk')"
    # future_result_set = dbclient.submitAsync(query)   # returns a CosmosDB Connection Message, no blocking
    # result_set = future_result_set.result()           # blocks until request written to Server and ResultSet constructed
    # result = result_set.one()
    # assert result_set.done.done()
    # if result_set.result() is None:
    #     raise Exception("CosmosDB Error: {}".format(query))
    # print(result)

    ################################################
    # 10/2021
    # CosmosDB does not yet support:
    #   Bytecode
    #   GraphSON serializer v3
    # following code will not work until then
    # g = traversal().withRemote(DriverRemoteConnection('wss://word-knowledge-db.gremlin.cosmos.azure.com:443/', 'g', username='/dbs/WordKnowledge/colls/WordSense', password='nioOwS9IVVs1kEsXhQ65lfSP5jD5ZKRIOAQYUpAIC3I2ZsZvZo5AFfZtJkgtrW0zhTn6uEPGTNSRDYwZXcCxUg==', message_serializer=serializer.GraphSONSerializersV2d0()))
    # test = g.V().toList()
    # test = g.addV('person').property('pk', '/pk').property('id', 'ME').toList()
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