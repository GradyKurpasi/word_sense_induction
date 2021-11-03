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

def write_source(client, source_id, source_type, source_year, source_desc):
    query = "g.addV('source').property('id', '{}').property('type', '{}').property('year', '{}').property('description', '{}').property('pk', '/pk')".format(
        source_id, source_type, source_year, source_desc)
    callback = client.submitAsync(query)
    if callback.result() is None:
        raise Exception("CosmosDB Error: {}".format(query))


def write_lemma(client, lemma, token, address, pos, source_id):
    query = ["g.addV('lemma').property('id', '{}').property('pk', '/pk')".format(lemma), 
            "g.V().hasLabel('lemma').has('id', '{}').addE('occursIn').property('id', '{}').property('token', '{}').property('pos', '{}').to(g.V().hasLabel('source').has('id', '{}'))".format(
                lemma, address, token, pos, source_id)]
    for string in query:
        callback = client.submitAsync(string)
        if callback.result() is None:
            raise Exception("CosmosDB Error: {}".format(query))


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
                    token = word.text
                    if 'lemma' in word.attrib.keys():
                        lemma = word.attrib['lemma']
                        lemma_set.add(lemma)
                        lemma_count += 1
                        address = word.attrib['id']
                        pos = word.attrib['pos']
                        write_lemma(dbclient, lemma, token, address, pos, source_id)
        dbclient.close()
        print("Word Count: {}".format(word_count))
        print("Lemma Count: {}".format(lemma_count))
        print("# of Unique Lemma: {}".format(len(lemma_set)))
        # Database is missing 1 Lemma and about 100 lemma/document edges

    except Exception as e:
        raise Exception(e)    
    finally:
        dbclient.close()
        print("Database closed")



def import_semeval2015_keys():
    multi_word = 0
    key_reader = open_semeval2015_keys()
    print(key_reader)
    for line in key_reader:
        if line[0] != line[1]: multi_word += 1
        print(line[0])
        print(line[1])
        print(line[2])
        print(len(line))
        for i in range(3, len(line)):
            print(line[i])
            
    print("Lines: {}".format(key_reader.line_num))
    print("Multi Word: {}".format(multi_word))