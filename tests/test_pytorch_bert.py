from  interfaces.adapters_pytorch_bert import *



def test_sum_all_hidden_layers(target_embedding, hidden_layers, tgt_word, batch=0):
    """ensures hidden layers summed correctly"""
    tgt_embedding = torch.empty_like(hidden_layers[0][batch][tgt_word])
    with open('output.txt', 'w') as f:
        f.write("HIDDEN LAYERS\n")
        f.write(str(hidden_layers))
        f.write("\n\n")
        i = 0
        for layer in hidden_layers:
            f.write('\nLAYER_EMBEDDING ' + str(i))
            f.write(str(layer[batch][tgt_word]))
            tgt_embedding += layer[batch][tgt_word]
            f.write('\nTGT EMBEDDING ' + str(i))
            f.write(str(tgt_embedding))
            i += 1
    assert len(tgt_embedding)==768
    assert torch.all(torch.eq(tgt_embedding, target_embedding))

    
def test_sum_last4_hidden_layers(target_embedding, hidden_layers, tgt_word, batch=0):
    """ensures last 4 hidden layers summed correctly"""
    tgt_embedding = torch.empty_like(hidden_layers[0][batch][tgt_word])
    with open('output.txt', 'w') as f:
        f.write("HIDDEN LAYERS\n")
        f.write(str(hidden_layers))
        f.write("\n\n")
        i = 0
        for layer in hidden_layers[-4:]:
            f.write('\nLAYER_EMBEDDING ' + str(i))
            f.write(str(layer[batch][tgt_word]))
            tgt_embedding += layer[batch][tgt_word]
            f.write('\nTGT EMBEDDING ' + str(i))
            f.write(str(tgt_embedding))
            i += 1
    # assert len(tgt_embedding)==768
    assert len(tgt_embedding)==len(hidden_layers[0][batch][tgt_word])
    assert torch.all(torch.eq(tgt_embedding, target_embedding))



def test_concat_last4_hidden_layers(target_embedding, hidden_layers, tgt_word, batch=0):
    """ensures last 4 hidden layers concantenated correctly"""
    tgt_embedding = torch.empty(0)
    with open('output.txt', 'w') as f:
        f.write("HIDDEN LAYERS\n")
        f.write(str(hidden_layers))
        f.write("\n\n")
        i = 0
        for layer in hidden_layers[-4:]:
            f.write('\nLAYER_EMBEDDING ' + str(i))
            f.write(str(layer[batch][tgt_word]))
            tgt_embedding = torch.cat((tgt_embedding, layer[batch][tgt_word]))
            f.write('\nTGT EMBEDDING ' + str(i))
            f.write(str(tgt_embedding))
            i += 1
        f.write("LENGTH = " + str(tgt_embedding.shape))
    assert len(tgt_embedding)==768*4
    assert len(tgt_embedding)==len(hidden_layers[0][batch][tgt_word]) * 4
    assert torch.all(torch.eq(tgt_embedding, target_embedding))









