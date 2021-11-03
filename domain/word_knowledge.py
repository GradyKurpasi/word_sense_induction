



class Sense():

    def __init__(self, sense_id, source, gloss="") -> None:
        self.sense_id = sense_id
        self.source = source
        self.gloss = gloss
    
    def __str__(self) -> str:
        return (str([self.sense_id, self.source, self.gloss]))


class LemmaDict():
    
    def __init__(self) -> None:
        self.lemma = set(())
        self.tokens = {}
        self.senses = {}

    def add_lemma(self, lemma):
        """
            adds lemma to lemma set
        """
        self.lemma.add(lemma)
    
    def add_token(self, lemma, token):
        """
            adds lemma (if necessary) and associated token
        """
        self.lemma.add(lemma)
        if lemma not in self.tokens.keys(): # initialize token set if necessary
            self.tokens[lemma] = set(()) 
        self.tokens[lemma].add(token)

    def add_sense(self, lemma, sense:Sense):
        self.lemma.add(lemma)
        if lemma not in self.senses.keys(): # initialize sense set if necessary
            self.senses[lemma] = set(())
            self.senses[lemma].add(sense)
            # return
        for sense_item in self.senses[lemma]: # check for identical sense already mapped to this lemma
            if (sense.sense_id==sense_item.sense_id and sense.source==sense_item.source):
                sense_item.gloss = sense.gloss
                break
        else:
            self.senses[lemma].add(sense)
    
    def __str__(self) -> str:
        return_str = ""
        for lemma in self.lemma:
            return_str += "\nLemma: " + lemma 
            return_str += "\nTokens: " + ( str(self.tokens[lemma]) if lemma in self.tokens.keys() else "" )
            return_str += "\nSenses: "
            if lemma in self.senses.keys():
                sense_list = list(self.senses[lemma])
                for i in range(0, len(sense_list)): 
                    return_str += "\n" + str(sense_list[i])
        return return_str





