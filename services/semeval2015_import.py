from interfaces.adapter_cosmosdb import *

from domain.word_knowledge import LemmaDict
import xml.etree.ElementTree as ET
import csv
import json

DATA_FILE = "./SemEval-2015/data/semeval-2015-task-13-en.xml"
KEY_FILE = "./SemEval-2015/keys/gold_keys/EN/semeval-2015-task-13-en.key"
ADDR_PREFIX = "semeval2015."


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
    """
        reads semeval2015 data from XML tree reader
        inserts source vertices
        inserts lemma vertices
        inserts lemma->source occursIn edges
    """
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
            # build source id
            source_id = "semeval2015-" + document.attrib['id']
            # build description
            if document.attrib['id']=="d001": description = "Biomedical information about drugs"
            elif document.attrib['id']=="d002": description = "Biomedical information about drugs"
            elif document.attrib['id']=="d003": description = "Calculator instruction manual"        
            elif document.attrib['id']=="d004": description = "Social issue discussion"
            # write source document vertices
            write_source(dbclient, source_id, "semeval2015 corpus", "2015", description)
            print(document.attrib['id'])

            for sentence in document:
                print(sentence.attrib['id'])

                for word in sentence:
                    word_count += 1
                    # build lemma and token strings
                    token = word.text.replace("'", "[UTF-8 39 decimal]").replace("?", "[UTF-8 63 decimal]")   # escapes single quote and questionmark
                    if 'lemma' in word.attrib.keys():
                        lemma = word.attrib['lemma'].replace("?", "[UTF-8 63 decimal]")
                        lemma_count += 1
                        address = ADDR_PREFIX + word.attrib['id']
                        pos = word.attrib['pos']
                        # write lemma vertices
                        if lemma not in lemma_set:
                            
                            write_lemma(dbclient, lemma)
                            lemma_set.add(lemma)
                        # write lemma->sources occursIn edges
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

def parse_key_address(address):
    doc = int(address[1:4])
    sent = int(address[6:9])
    tok = int(address[11:])
    return doc, sent, tok


def format_address(doc, sent, tok):
    return "d" + str(doc).rjust(3,'0') + ".s" + str(sent).rjust(3,'0') + ".t" + str(tok).rjust(3,'0')


def update_edge(client, address, sense_id):
    query = "g.E().has('id', '{}').property('checked', 'true').property('sense', '{}')".format(address, sense_id)
    result_set = client.submit(query)
    edges = result_set.all().result() #blocking call
    return edges
    

def write_sense(client, query):
    """ Synchronously writes source vertex to graph """
    result_set = client.submit(query)   # blocks until request written to server
    results = result_set.all().result() # blocks until results returned from server
    assert result_set.done.done()
    if result_set is None:
        raise Exception("CosmosDB Error: {}".format(query))
    return results

def write_lemma_sense_edge(client, lemma, sense_id):
    """Synchronsously writes lemma->sense edges and sense->lemma edges"""
    query = "g.V().hasLabel('lemma').has('id', '{}').addE('hasSense').to(g.V().hasLabel('sense').has('id', '{}'))".format(lemma, sense_id)
    result_set = client.submit(query)   # blocks until request written to server
    results = result_set.all().result() # blocks until results returned from server
    assert result_set.done.done()
    if result_set is None:
        raise Exception("CosmosDB Error: {}".format(query))
    return results


def write_sense_lemma_edge(client, sense_id, lemma):
    query = "g.V().hasLabel('sense').has('id', '{}').addE('hasLemma').to(g.V().hasLabel('lemma').has('id', '{}'))".format(sense_id, lemma)
    result_set = client.submit(query)   # blocks until request written to server
    results = result_set.all().result() # blocks until results returned from server
    assert result_set.done.done()
    if result_set is None:
        raise Exception("CosmosDB Error: {}".format(query))
    return results


def cleanup_key_import(dbclient):
    dbclient.submit("g.V().hasLabel('sense').drop()")
    dbclient.submit("g.E().hasLabel('hasSense').drop()")
    dbclient.submit("g.E().hasLabel('hasLemma').drop()")



def import_semeval2015_keys():
    multi_word = 0
    multi_words = []
    missing_edge = 0
    missing_edges = []
    edges_checked = 0
    sense_set = set(())
    lemma_sense_set = set(())
    key_reader = open_semeval2015_keys()
    dbclient = connect_cosmosdb_client()
    # cleanup_key_import(dbclient)
    try:
        for line in key_reader:
            start_address = line[0]
            end_address = line[1]
            sense_id = line[2]
            start_doc, start_sent, start_tok = parse_key_address(start_address)
            end_doc, end_sent, end_tok = parse_key_address(end_address)
            # build sense insert query
            sense_insert_string = "g.addV('sense').property('pk', '/pk').property('source', 'semeval2015').property('id', '{}')".format(sense_id)
            for i in range(2, len(line)):
                source = line[i].split(":", 1)[0]
                id = line[i].split(":", 1)[1]
                sense_insert_string += ".property(list, '{}', '{}')".format(source, id)
            # write sense
            if sense_id not in sense_set:
                write_sense(dbclient, sense_insert_string)
            sense_set.add(sense_id)

            # debug code, check for multi-word lemma
            if start_tok == end_tok: 
                end_tok += 1
            else:
                multi_word += 1
                multi_words.append([start_address, end_address])
            # insert sense data into lemma-> sense occursIn edges
            for tok in range(start_tok, end_tok):
                edges_checked += 1
                address = ADDR_PREFIX + format_address(start_doc, start_sent, tok)
                edges = update_edge(dbclient, address, sense_id) 
                for edge in edges:
                    lemma = edge['outV']
                    if (lemma, sense_id) not in lemma_sense_set:
                        # create lemma-> sense edges and edge-> lemma sense
                        write_lemma_sense_edge(dbclient, lemma, sense_id)
                        # create sense-> lemma edges
                        write_sense_lemma_edge(dbclient, sense_id, lemma)
                        lemma_sense_set.add((lemma, sense_id))

            print("Line: {}".format(key_reader.line_num))

            # DEVELOPMENT CODE
            # if line[0] != line[1]: 
            #     multi_word += 1
            #     multi_words.append([line[0], line[1]])
            #     print(parse_key_address(line[0]))
            #     print(parse_key_address(line[1]))
            #     print("\n")

        print("Lines: {}".format(key_reader.line_num))
        print("Multi Word: {}".format(multi_word))
        # print(multi_words)

    except Exception as e:
        raise Exception(e)    
    finally:
        print("Current Address: {}".format(start_address))
        print("Edges Checked: {}".format(edges_checked))
        print("Missing Edges: {}".format(missing_edge))
        print(missing_edges)
        dbclient.close()
        print("Database closed")




    # g.V().outE().has('id', containing('d001.s001'))
    # g.E().hasNot('checked')

def find_edge(client, address):
    query = "g.E().has('id', '{}')".format(address)
    result_set = client.submit(query)
    edges = result_set.all().result() #blocking call
    return edges
    


class PadList(list):
    def ljust(self, n, fillvalue=''):
        return self + [fillvalue] * (n - len(self))

    def rjust(self, n, fillvalue=''):
        return [fillvalue] * (n-len(self)) + self



def preprocess_semeval2015_documents():
    """
        reads semeval2015 text from XML tree reader
        creates 3 representations of words
        list of words in document order
        list of sentences (list of words)
        map of lemma to occurrence addresses
    """
    semeval_data = open_semeval2015_data()
    token_count = 0         # count of all tokens in all documents
    lemma_count = 0         # count of all lemma in all documents
    lemma_set = set(())     # all lemma in all documents
    lemma_map = {}          # occurrences of lemma in all documents
    docs = []
    dbclient = connect_cosmosdb_client()
    no_sense = set(())

    for document in semeval_data.getroot():
        doc_token_count = 0         # of tokens in doc
        # doc_lemma_count = 0
        # doc_lemma_set = set(())
        sent_count = 0              # of sentences in doc
        tokenlist = []              # list of tokens in doc (essentially recreation of text)
        source_id = "semeval2015-" + document.attrib['id']
        print(document.attrib['id'])
        doc = []
        if document.attrib['id'] == 'd003': # document3 starts at sentence 2, no sentence 1
            doc.append("")                 # add a blank sentence
        for sentence in document:       
            print(sentence.attrib['id'])
            sent = []
            sent_count += 1
            for word in sentence:
                # update counts
                token_count += 1
                doc_token_count += 1
                # format token
                token = word.text.replace("'", "[UTF-8 39 decimal]").replace("?", "[UTF-8 63 decimal]")   # escapes single quote and questionmark
                # add token to lists
                sent.append(token)
                tokenlist.append(token)
                # if token is a lemma - update lemma stats and lists
                if 'lemma' in word.attrib.keys():
                    lemma = word.attrib['lemma'].replace("?", "[UTF-8 63 decimal]")
                    address = word.attrib['id']
                    print(lemma)

                    # get existing edges to find sense key (disambiguation answer)
                    edge = find_edge(dbclient, ADDR_PREFIX + address)
                    assert len(edge) == 1
                    # not all lemma had sense keys in answer set if no sense key exists, skip lemma altogether
                    if 'sense' not in edge[0]['properties'].keys():
                        no_sense.add(lemma)
                        print("Missing Sense {}".format(lemma))
                        continue
                    # if lemma in ('be', 'epar', 'unresectable', 'have', 'own', 'qualify', 'recommended', 'receive', 'b12', 'anti-emetic', 'characteristics', 'do', 'work', 'such as', 'comparator'):
                    #     continue
                    lemma_count += 1

                    # find occursIn edge to get sense_id solution                    
                    sense = edge[0]['properties']['sense']

                    # record lemma
                    if lemma not in lemma_set:
                        lemma_map[lemma] = {address : sense}
                    else:
                        lemma_map[lemma][address] = sense
                    lemma_set.add(lemma)
            doc.append(sent)
        docs.append(doc)
    
    dbclient.close()
    print("DONE W PRE-PROCESSING")
    print("No Sense: ", no_sense)

    print("Writing document to json")
    # save document data to json
    with open('semeval2015-docs.json', 'w') as f:
        json.dump(docs, f, indent = 2)
 
    # save lemma data to json
    # set objects are not json serializable
    print("writing lemma set")
    with open("lemma_set.json", "w") as f:
        json.dump(list(lemma_set), f, indent=2)

    # save lemma map to json
    # set objects are not json serializable
    print("writing lemma map")
    lemma_map_json = {}
    for key, val in lemma_map.items():
        lemma_map_json[key] = list(val.items())
    with open("lemma_map.json", "w") as f:
        json.dump(lemma_map_json, f, indent=2)
    print("Total Words: {}".format(token_count))    







def create_left_aligned_sentences():
    """
        create 1 left aligned sentence for every sense coded lemma (not all lemma have sense mappings)
    """
    # Load Lemma Map
    # Lemma Map
    #      lemma : [
    #               [address, sense]
    #               [address, sense]
    #               [address, sense] 
    #               ]
    #      lemma : [
    #               [address, sense]
    #               ]
    # etc.
    print("Loading Lemma Data")
    with open('lemma_map.json', ) as f:
        lemma_map = json.load(f)
    with open ('semeval2015-docs',) as f:
        docs = json.load(f)    
    print("Creating Left Aligned sentences")
    max_len = 0
    sent_out = []
    for lemma, occurence_list in lemma_map.items():
        for occurrence in occurence_list:
            address = occurrence[0]
            sense = occurrence[1]
            docid, sentid, tokid = parse_key_address(address)
            sent = docs[docid-1][sentid-1]
            sent_out.append([lemma,  sense, str(tokid), sent])

    print("Save JSON")
    with open("sent_left.json", "w") as f:
        json.dump(sent_out, f, indent=2)










def create_centered_sentences():
    """
        create 1 centered sentence for every sense coded lemma (not all lemma have sense mappings)
    """
    print("Loading Lemma Data")
    with open('lemma_map.json', ) as f:
        lemma_map = json.load(f)
    with open ('semeval2015-docs',) as f:
        docs = json.load(f)  
    print("Creating centered sentences")
    max_len = 0
    sent_out = PadList()
    context_center = 100
    for lemma, occurence_list in lemma_map.items():
        for occurrence in occurence_list:
            address = occurrence[0]
            sense = occurrence[1]
            docid, sentid, tokid = parse_key_address(address)
            sent = docs[docid-1][sentid-1]
            sent_left = PadList(sent[:tokid-1])
            sent_right = PadList(sent[tokid:])
            sent = sent_left.rjust(context_center, '') + [lemma] + sent_right.ljust(context_center, '')
            assert len(sent) == (2 * context_center) + 1
            assert sent[context_center] == lemma
            sent_out.append([lemma,  sense, str(context_center), sent])

    print("Save JSON")
    with open("sent_center.json", "w") as f:
        json.dump(sent_out, f, indent=2)




def create_centered_contexts():
    """
        create 1 centered context for every sense coded lemma (not all lemma have sense mappings)
        appends surrounding sentences on right and left then trims to context_width
    """
    print("Loading Lemma Data")
    with open('lemma_map.json', ) as f:
        lemma_map = json.load(f)
    with open ('semeval2015-docs',) as f:
        docs = json.load(f)  
    print("Creating centered sentences")
    max_len = 0
    sent_out = PadList()
    context_width = 100
    for lemma, occurence_list in lemma_map.items():
        for occurrence in occurence_list:
            address = occurrence[0]
            sense = occurrence[1]
            docid, sentid, tokid = parse_key_address(address)
            sent = docs[docid-1][sentid-1]
            sent_left = PadList(sent[:tokid-1])
            sent_right = PadList(sent[tokid:])

            for i in range(1, 10):  #expand context left and right of current sentence
                try:
                    sent_left = docs[docid-1][sentid-1-i] + [" "] + sent_left
                    sent_right = sent_right + [" "] + docs[docid-1][sentid-1+i]
                except:
                    pass
            if len(sent_left) < context_width: 
                sent_left = PadList(sent_left).rjust(context_width, '') 
            if len(sent_right) < context_width: 
                sent_right = PadList(sent_right).ljust(context_width, '')

            sent = sent_left[-context_width:] + [lemma] + sent_right[:context_width]
            assert len(sent) == (2 * context_width) + 1
            assert sent[context_width] == lemma
            sent_out.append([lemma,  sense, str(context_width), sent])

    print("Save JSON")
    with open("context_center.json", "w") as f:
        json.dump(sent_out, f, indent=2)


    # PART Iv
    # create centered contexts
    # print("Creating centered contexts")
    # context_size = 100
    # sent_out = PadList()
    # lenlem = len(lemma_set)
    # lem = 0
    # for lemma in lemma_set:
    #     lem += 1
    #     print("Lemma: {} of {}".format(lem, lenlem))
    #     for lemma, address_list in lemma_map.items():
    #         for address in address_list:
    #             docid, sentid, tokid = parse_key_address(address)
    #             sent = docs[docid-1][sentid-1]
    #             sent_left = PadList(sent[:tokid-1])
    #             sent_right = PadList(sent[tokid:])
    #             for i in range(1, 10):  #expand context left and right of current sentence
    #                 try:
    #                     sent_left = docs[docid-1][sentid-1-i] + [" "] + sent_left
    #                     sent_right = sent_right + [" "] + docs[docid-1][sentid-1+i]
    #                 except:
    #                     pass
    #             if len(sent_left) < context_size: 
    #                 sent_left = PadList(sent_left).rjust(context_size, '') 
    #             if len(sent_right) < context_size: 
    #                 sent_right = PadList(sent_right).ljust(context_size, '')




    #             sent = sent_left[-context_size:] + [lemma] + sent_right[:context_size]
    #             assert len(sent) == (2 * context_size) + 1
    #             assert sent[context_size] == lemma
    #             sent_out.append(sent)
    # # lemma_map_json = dict(zip(lemma_map.keys(), list(lemma_map.values())))
    # with open("context_center.json", "w") as f:
    #     json.dump(sent_out, f, indent=2)
    # print("DONE")

