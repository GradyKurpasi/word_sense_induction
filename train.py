import transformers
from interfaces.adapter_cosmosdb import *
from interfaces.adapters_pytorch_bert import *
from domain.gng import *
from domain.word_knowledge import LemmaDict
from azureml.core.dataset import Dataset
import json


DEFAULT_LEMMA_MAP = 'semeval-2015/lemma_map.json'
DEFAULT_DATASET = 'semeval-2015/sent_center.json'
DEFAULT_LEMMA = 'use'


def open_dataset(dataset = DEFAULT_DATASET):
    with open(dataset, ) as f:
        ds = json.load(f)
    return ds

def create_embeddings(target_lemma = DEFAULT_LEMMA):


    # MODEL
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    EMBEDDING_SIZE = 768


    # PREPARE INPUT FROM DATASET
    """ tokenizer expects list of strings"""
    input_text = []    
    answer_key = [] 
    se2015_data = open_dataset()
    # se2015_data = open_dataset('semeval-2015/sent_center.json')
    # se2015_data = open_dataset('semeval-2015/context_center.json')

    # for row in se2015_data:
    #     input_text.append(" ".join(row[3]))

    # data file format [lemma, sense, lemma_address, [context string] ]

    for row in se2015_data:
        lemma = row[0]
        sense = row[1]
        senseid = row[2]
        if lemma == target_lemma:
            input_text.append(" ".join(row[3]))
            answer_key.append([lemma, sense, senseid])
    assert len(input_text) == len(answer_key)


    # TEST CODE
    # input_text = ['I am Groot', 'Its a small world afterall']
    # answer_key = [['am', 'bnxxx', '2'], ['small', 'bnxxx', '3']]

    # TOKENIZER
    inputs = tokenizer(input_text, padding=True, truncation=True, return_tensors='pt')    # returns: {'input_ids' : [tensor], 'token_type_ids' : [tensor], 'attention_mask' : [tensor]}


    # MODEL OUTPUTS
    # outputs = model(**input)
    outputs = model(**inputs, output_hidden_states=True)
    sentence_embeddings = outputs['last_hidden_state']
    # outputs['last_hidden_state].shape = batch size (# sentences)  X  sequence length (# of words)  X  embedding size (# of self attention nodes)
    # outputs[x][0] = sentence classifier
    # outputs[x][1] = first word
    
    
    # data = outputs['last_hidden_state'].view(-1, 768)     # this line will collapse all embeddings into one array (not currently in use)

    target_embeddings = []    #torch.empty(0)
    assert len(answer_key) == len(sentence_embeddings)
    for key, embedding in zip(answer_key, sentence_embeddings):
        tgt = int(key[2])
        target_embeddings.append(embedding[tgt])
        # target_embeddings = torch.cat((target_embeddings, embedding[tgt]))
    

    target_embeddings = torch.stack(target_embeddings)
    filename = "semeval2015_" + target_lemma + "_embeddings.pt"
    torch.save(target_embeddings, filename)
    print(target_embeddings.shape)
    print("Embeddings {}".format(len(answer_key)))
    print("DONE")
    return target_embeddings




def create_clusters():


    print("Creating Clusters")
    filename = "semeval2015_use_embeddings.pt"
    data = torch.load(filename)
    print(data.shape)

    gng = GrowingNeuralGas(data)
    gng.fit_network(e_b=0.1, e_n=0.006, a_max=10, l=200, a=0.5, d=0.995, passes=10000, plot_evolution=True)
    print('Found %d clusters.' % gng.number_of_clusters())
    # gng.plot_clusters(gng.cluster_data())
    nodes = gng.get_nodes()
    node_ten = torch.Tensor(nodes)
    export_embeddings_to_tensorboard(nodes)


# simple_model()
# example_simple_model_multiple_inputs()
# example_gng()
# example_multiple_paired_inputs()

