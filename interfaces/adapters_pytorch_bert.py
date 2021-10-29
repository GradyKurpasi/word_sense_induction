"""
Pytorch Transformers code provided by Hugging Face under Apache 2.0 license
Copyright 2018- The Hugging Face team. All rights reserved.
"""
import torch
from torch import Tensor
from transformers import AutoTokenizer, AutoModel, pipeline, BertTokenizer, BertModel, BertForNextSentencePrediction, BertConfig
from transformers.utils.dummy_pt_objects import LayoutLMPreTrainedModel


def print_inputs(input_text, inputs):
    """
        expects input format: {'input_ids' : [[tensor]], 'token_type_ids' : [[tensor]], 'attention_mask' : [[tensor]]}
    """
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    print('\n\nINPUT TEXT')
    print(input_text)
    print('\nINPUTS')
    print (inputs)
    print(f'Length of BERT base vocabulary: {len(tokenizer.vocab)}')
    sent_count = 1
    for tensors in inputs['input_ids']:
        print('\nSentence: ' + str(sent_count))
        print('Tokens: ' + str(len(tensors)))
        word_count = 0
        for tokens in tensors:
            print(f'Token {str(word_count)}: {tokens}, subword: {tokenizer.decode([tokens])}')
            word_count += 1
        sent_count += 1

def first_hidden_layer(hidden_layers, tgt_word, batch=0):
    """
        expects hidden_layers = tuple of tensors
            len hidden_layers = N + 1 (bert_base = 13, bert_large=25)    
            dim tensors = batch x sequence_length (sentence) x embedding_size
    """
    layer = 0
    tgt_embedding = hidden_layers[layer][batch, tgt_word, :]    # slice 3D tensor by batch and word (return tgt_words full embedding)
    return tgt_embedding

def last_hidden_layer(hidden_layers, tgt_word, batch=0):
    """
        expects hidden_layers = tuple of tensors
            len hidden_layers = N + 1 (bert_base = 13, bert_large=25)    
            dim tensors = batch x sequence_length (sentence) x embedding_size
    """
    layer = len(hidden_layers) - 1
    tgt_embedding = hidden_layers[layer][batch, tgt_word, :]    # slice 3D tensor by batch and word (return tgt_words full embedding)
    return tgt_embedding

def sum_all_hidden_layers(hidden_layers, tgt_word, batch=0):
    """
        expects hidden_layers = tuple of tensors
            len hidden_layers = N + 1 (bert_base = 13, bert_large=25)    
            dim tensors = batch x sequence_length (sentence) x embedding_size
    """
    tgt_embedding = torch.empty_like(hidden_layers[0][batch][tgt_word])
    for layer in hidden_layers:
        tgt_embedding += layer[batch][tgt_word]
    return tgt_embedding


def sum_last4_hidden_layers(hidden_layers, tgt_word, batch=0):
    """
        expects hidden_layers = tuple of tensors
            len hidden_layers = N + 1 (bert_base = 13, bert_large=25)    
            dim tensors = batch x sequence_length (sentence) x embedding_size
    """
    tgt_embedding = torch.empty_like(hidden_layers[0][batch][tgt_word])
    for layer in hidden_layers[-4:]:
        tgt_embedding += layer[batch][tgt_word]
    return tgt_embedding

def concat_last4_hidden_layers(hidden_layers, tgt_word, batch=0):
    """
        expects hidden_layers = tuple of tensors
            len hidden_layers = N + 1 (bert_base = 13, bert_large=25)    
            dim tensors = batch x sequence_length (sentence) x embedding_size
    """
    tgt_embedding = torch.empty(0)
    for layer in hidden_layers[-4:]:
        tgt_embedding = torch.cat((tgt_embedding, layer[batch][tgt_word]))
    return tgt_embedding



def print_outputs(outputs):
    """
        expectes BertModel Output object
    """
    print("\n\nOUTPUTS\n\n")
    print(f'output type: {type(outputs)}, output length: {len(outputs)}')

    # sequence_length = sentence length
    # embedding size = 768 for bert_base, 1024 for bert_large (also called hidden_size)

    # Output: Last Hidden State = outputs[0]
    #   dims = batch size x sequence length x embedding size (e.g. 1 x 5 x 768)
    print('\nLast Hidden State shape: ' + str(outputs['last_hidden_state'].shape))    
    
    # Output: Pooler Output = outputs[1]
    #   corresponds to [CLS] (classifier token / first token)
    #   pooled output represents whole sequence 
    #   dims = batchsize x embedding size (e.g. 1 x 768)
    print('\nPooler Output shape: ' + str(outputs['pooler_output'].shape))
    
    # Output: Hidden States dims = outputs [2]
    #   Tuple of Tensors
    #   Len = N layers + 1 output layer
    #   N = (bert_base = 12, bert_large = 24)
    print('\nLen Hidden States tuple: ' + str(len(outputs['hidden_states'])))
    #   dims of tensors = batchsize x sequence length x embedding size (e.g. 1 x 5 x 768)
    print('\nHidden States tensor shape: ' + str(outputs['hidden_states'][0].shape))


    # mean of all sequence embeddings (i.e. entire sentence), shape = 1 x 768
    seq_mean = outputs['last_hidden_state'].mean(1)
    print("\nMean of all word embeddings for sentence 1:")
    # print(seq_mean)


    print(outputs['hidden_states'])
    print("\n\n")
    tgt_batch = 0
    tgt_word = 1



    first_layer = first_hidden_layer(outputs['hidden_states'], tgt_word, tgt_batch)
    # assert torch.all(torch.eq(outputs['hidden_states'][0][0][1], first_layer))

    last_layer = last_hidden_layer(outputs['hidden_states'], tgt_word, tgt_batch)
    # assert torch.all(torch.eq(outputs['hidden_states'][12][0][1], last_layer))
    # assert torch.all(torch.eq(outputs['last_hidden_state'], outputs['hidden_states'][12]))

    sum_all_layers = sum_all_hidden_layers(outputs['hidden_states'], tgt_word, tgt_batch)
    sum_last4_layers = sum_last4_hidden_layers(outputs['hidden_states'], tgt_word, tgt_batch)
    concat_last4_layers = concat_last4_hidden_layers(outputs['hidden_states'], tgt_word, tgt_batch)








def simple_model():
    # MODEL
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")

    #INPUT
    input_text = 'Hello There!'

    # TOKENIZER
    # tokens = tokenizer(text)  # returns: {'input_ids' : [list], 'token_type_ids' : [list], 'attention_mask' : [list]}
    inputs = tokenizer(input_text, return_tensors='pt')   # returns: {'input_ids' : [tensor], 'token_type_ids' : [tensor], 'attention_mask' : [tensor]}
    print_inputs(input_text, inputs)
    
    # MODEL OUTPUTS
    # outputs = model(**input)
    outputs = model(**inputs, output_hidden_states=True)
    print_outputs(outputs)




def simple_model_multiple_inputs():
    # MODEL
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    #INPUT
    text = ['Hello There!', 'Goodbye for now.']

    # TOKENIZER
    tokens = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    print (tokens)
    print(f'Length of BERT base vocabulary: {len(tokenizer.vocab)}')
    print(f'Text: {text}')
    for inputs in tokens['input_ids']:
        for t in inputs:
            print(f'Token: {t}, subword: {tokenizer.decode([t])}')
    print(len(tokens['input_ids']))

    # BATCHING 
    # unsqueeze adds a singleton at specified dimension
    # used to set batch size of input
    # inputs = torch.tensor(tokens).unsqueeze(0) # Batch size 1

    # MODEL OUTPUTS
    outputs = model(**tokens)
    print(f'output type: {type(outputs)}, output length: {len(outputs)}')
    # Output 1 dims = batch size x sequence length x 768 (embedding size or hidden size)
    print(f'first item shape: {outputs[0].shape}')
    # Output 2 dims = batchsize x 768 (pooled output - represents whole sequence / correspondes to [CLS] token)
    print(f'second item shape: {outputs[1].shape}')
    # mean of sequence embeddings = 1 x 768 (embedding size or hidden size)
    seq_mean = outputs[0].mean(1)
    print(outputs)




def paired_inputs():
    # MODEL
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    # TOKENIZER
    encoded_input = tokenizer("How old are you?", "I'm 6 years old")
    print(encoded_input)

    # MODEL OUTPUTS
    outputs = model(**encoded_input)
    print(f'output type: {type(outputs)}, output length: {len(outputs)}')
    # Output 1 dims = batch size x sequence length x 768 (embedding size or hidden size)
    print(f'first item shape: {outputs[0].shape}')
    # Output 2 dims = batchsize x 768 (pooled output - represents whole sequence / correspondes to [CLS] token)
    print(f'second item shape: {outputs[1].shape}')
    # mean of sequence embeddings = 1 x 768 (embedding size or hidden size)
    # seq_mean = outputs[0].mean(1)
    print(outputs)


def multiple_paired_inputs():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    batch_sentences = ["Hello I'm a single sentence",
                   "And another sentence",
                   "And the very very last one"]
    batch_of_second_sentences = ["I'm a sentence that goes with the first sentence",
                             "And I should be encoded with the second sentence",
                             "And I go with the very last one"]
    encoded_inputs = tokenizer(batch_sentences, batch_of_second_sentences)
    print(encoded_inputs)
    print(encoded_inputs['input_ids'][0])
    for t in encoded_inputs['input_ids'][0]:
        print(f'Token: {t}, subword: {tokenizer.decode([t])}')
    print(len(encoded_inputs['input_ids'][0]))
    print(encoded_inputs['token_type_ids'][0])


def masked_language_model():
    # MASKED LANGUAGE MODEL EXAMPLE
    nlp = pipeline("fill-mask")
    preds = nlp(f"I am 'FUCKED', it's been a very {nlp.tokenizer.mask_token} day.")
    print('I am unhappy, it\'s been a very ***** day.')
    for p in preds: print(nlp.tokenizer.decode([p['token']]))



def next_sentence_prediction():
    # NEXT SENTENCE PREDICTION EXAMPLE
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')

    first_sentence = "I cut my finger."
    second_sentence_right = "The blood started flowing."
    second_sentence_wrong = "This website uses cookies."

    right = tokenizer.encode_plus(first_sentence, text_pair=second_sentence_right)
    wrong = tokenizer.encode_plus(first_sentence, text_pair=second_sentence_wrong)

    r1, r2, r3 = torch.tensor(right['input_ids']).unsqueeze(0), torch.tensor(right['token_type_ids']).unsqueeze(0), torch.tensor(right['attention_mask']).unsqueeze(0)
    w1, w2, w3 = torch.tensor(wrong['input_ids']).unsqueeze(0), torch.tensor(wrong['token_type_ids']).unsqueeze(0), torch.tensor(wrong['attention_mask']).unsqueeze(0)

    right_outputs = model(input_ids=r1, token_type_ids=r2, attention_mask=r3)
    right_seq_relationship_scores = right_outputs[0]
    wrong_outputs = model(input_ids=w1, token_type_ids=w2, attention_mask=w3)
    wrong_seq_relationship_scores = wrong_outputs[0]

    print(first_sentence + ' ' + second_sentence_right)
    print(f'Next sentence prediction: {right_seq_relationship_scores.detach().numpy().flatten()[0] > 0}')
    print(first_sentence + ' ' + second_sentence_wrong)
    print(f'Next sentence prediction: {wrong_seq_relationship_scores.detach().numpy().flatten()[0] > 0}')

    print("DONE")



    # MODEL
    tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased")
    model = AutoModel.from_pretrained("bert-large-uncased")
    model.config.output_attentions = True



# next_sentence_prediction()
# masked_language_model()





simple_model()
# simple_model_multiple_inputs()



