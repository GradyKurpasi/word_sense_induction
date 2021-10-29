import nltk
import transformers
import torch


from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased")
model = AutoModel.from_pretrained("bert-large-uncased")
# model.config.output_attentions = True




# inputs = tokenizer("Hello {SEP} world!", return_tensors="pt")
text = 'Hello There!'
tokens = tokenizer.encode(text)
print (tokens)

print(f'Length of BERT base vocabulary: {len(tokenizer.vocab)}')
print(f'Text: {text}')
for t in tokens:
    print(f'Token: {t}, subword: {tokenizer.decode([t])}')


print(len(tokens))


# unsqueeze adds a singleton at specified dimension
# used to set batch size of input
inputs = torch.tensor(tokens).unsqueeze(0) # Batch size 1

outputs = model(inputs)
print(f'output type: {type(outputs)}, output length: {len(outputs)}')

# Output 1 dims = batch size x sequence length x 768 (embedding size or hidden size)
print(f'first item shape: {outputs[0].shape}')
# Output 2 dims = batchsize x 768 (pooled output - represents whole sequence / correspondes to [CLS] token)
print(f'second item shape: {outputs[1].shape}')

# mean of sequence embeddings = 1 x 768 (embedding size or hidden size)
seq_mean = outputs[0].mean(1)



# outputs = model(**inputs)
# print(outputs)

print("DONE")


