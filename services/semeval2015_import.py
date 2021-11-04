from interfaces.adapter_cosmosdb import *

from domain.word_knowledge import LemmaDict
import xml.etree.ElementTree as ET
import csv

DATA_FILE = "./SemEval-2015/data/semeval-2015-task-13-en.xml"
KEY_FILE = "./SemEval-2015/keys/gold_keys/EN/semeval-2015-task-13-en.key"


#############################################
# File Handlers

def open_semeval2015_data(filename=DATA_FILE):
    """returns xml ElementTree"""
    with open(filename) as file:
        return ET.parse(file)


def open_semeval2015_keys(filename=KEY_FILE):
    """returns tab delimited fileobject"""
    # with open(filename, newline = '') as file:                                                                                          
    file = open(filename)                                                                                           
    return csv.reader(file, delimiter='\t')


#############################################
# Gremlin GraphDB Handlers
# 
# all writes use synchronous submits and blocking

def write_source(client, source_id, source_type, source_year, source_desc):
    """ Synchronously writes source vertex to graph"""
    query = "g.addV('source').property('id', '{}').property('type', '{}').property('year', '{}').property('description', '{}').property('pk', '/pk')".format(
        source_id, source_type, source_year, source_desc)
    result_set = client.submit(query)   # blocks until request written to server
    results = result_set.all().result() # blocks until results returned from server
    assert result_set.done.done()
    if result_set is None:
        raise Exception("CosmosDB Error: {}".format(query))
    return results

def write_lemma(client, lemma):
    """ Synchronously writes lemma vertex to graph """
    query = "g.addV('lemma').property('id', '{}').property('pk', '/pk')".format(lemma)
    result_set = client.submit(query)   # blocks until request written to server
    results = result_set.all().result() # blocks until results returned from server
    assert result_set.done.done()
    if result_set is None:
        raise Exception("CosmosDB Error: {}".format(query))
    return results


def write_occurence(client, lemma, token, address, pos, source_id):
    """ Synchronously writes occursIn edge from lemma to source """
    query = "g.V().hasLabel('lemma').has('id', '{}').addE('occursIn').property('id', '{}').property('token', '{}').property('pos', '{}').to(g.V().hasLabel('source').has('id', '{}'))".format(
                lemma, address, token, pos, source_id)
    result_set = client.submit(query)   # blocks until request written to server
    results = result_set.all().result() # blocks until results returned from server
    assert result_set.done.done()
    if result_set is None:
        raise Exception("CosmosDB Error: {}".format(query))
    return results




def __delete_entire_graph_database(client):
    query = "g.V().drop()"
    callback = client.submitAsync(query)
    if callback.result() is None:
        raise Exception("CosmosDB Error: {}".format(query))





def import_semeval2015_lemma():
    semeval_data = open_semeval2015_data()
    dbclient = connect_cosmosdb_client()
    word_count = 0
    lemma_count = 0
    lemma_set = set(())
    missing_edge_set = set(())
    try:
        __delete_entire_graph_database(dbclient)
        root = semeval_data.getroot()
        for document in root:
            source_id = "semeval2015-" + document.attrib['id']
            if document.attrib['id']=="d001": description = "Biomedical information about drugs"
            elif document.attrib['id']=="d002": description = "Biomedical information about drugs"
            elif document.attrib['id']=="d003": description = "Calculator instruction manual"        
            elif document.attrib['id']=="d004": description = "Social issue discussion"
            write_source(dbclient, source_id, "semeval2015 corpus", "2015", description)
            print(document.attrib['id'])
            for sentence in document:
                print(sentence.attrib['id'])
                for word in sentence:
                    word_count += 1
                    token = word.text.replace("'", "[UTF-8 39 decimal]").replace("?", "[UTF-8 63 decimal]")   # escapes single quote and questionmark
                    if 'lemma' in word.attrib.keys():
                        lemma = word.attrib['lemma'].replace("?", "[UTF-8 63 decimal]")
                        lemma_count += 1
                        address = word.attrib['id']
                        pos = word.attrib['pos']
                        if lemma not in lemma_set:
                            write_lemma(dbclient, lemma)
                            lemma_set.add(lemma)
                        write_occurence(dbclient, lemma, token, address, pos, source_id)
                        result_set = dbclient.submit('g.E().count()')
                        edges = result_set.all().result()[0] #blocking call
                        if edges != lemma_count:
                            print('Missing Edge: {}'.format(address))
                            missing_edge_set.add(address)
        dbclient.close()
        print("Word Count: {}".format(word_count))
        print("Lemma Count: {}".format(lemma_count))
        print("# of Unique Lemma: {}".format(len(lemma_set)))
        # Database is missing 1 Lemma and about 100 lemma/document edges

    except Exception as e:
        raise Exception(e)    
    finally:
        print(lemma, word_count, address)
        dbclient.close()

        print("Database closed")



def import_semeval2015_keys():
    multi_word = 0
    multi_words = []
    key_reader = open_semeval2015_keys()
    print(key_reader)
    for line in key_reader:
        if line[0] != line[1]: 
            multi_word += 1
            multi_words.append([line[0], line[1]])
        print(line[0])
        print(line[1])
        print(line[2])
        print(len(line))
        for i in range(3, len(line)):
            print(line[i])
            
    print("Lines: {}".format(key_reader.line_num))
    print("Multi Word: {}".format(multi_word))
    print(multi_words)



    # g.V().outE().has('id', containing('d001.s001'))