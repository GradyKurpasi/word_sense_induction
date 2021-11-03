"""
Natural Language Toolkit code is provided by nltk.org under the Apache 2.0 license
Copyright (C) 2001-2021 NLTK Project

WordNet code and binaries provided under license by Princeton University
WordNet 3.0 Copyright 2006 by Princeton University.  All rights reserved.
WordNet 1.6 Copyright 1997 by Princeton University.  All rights reserved. 
George A. Miller (1995). WordNet: A Lexical Database for English.
Communications of the ACM Vol. 38, No. 11: 39-41.
Christiane Fellbaum (1998, ed.) WordNet: An Electronic Lexical Database. Cambridge, MA: MIT Press.
Princeton University "About WordNet." WordNet. Princeton University. 2010. 

"""


from ports_sources import AbstractSource
from nltk.corpus import semcor





class NLTKSemcorSource(AbstractSource):
    """
    Thin wrapper for NLTK Semcor 3.0 corpus
    Semantically tagged subset of the Brown Corpus
    SemCor 3.0 was automatically created from SemCor 1.6 by mapping WordNet 1.6 to WordNet 3.0 senses.
    SemCor 1.6 was created by and is property of Princeton University.
    """
    
    def __init__(self): 
        super().__init__()
        self.semcor = semcor

    def open(self): # port function
        try:
            s = semcor.words()
            
        except LookupError as e:
            return "Error: NLTK SEMCOR Corpus Not Found"

        return "success"

    def close(self): # port function
        pass

    def read(self, segment): # port function
        if segment == 'word' or segment == 'simple':
            return semcor.words()
        elif segment == 'chunk':
            return semcor.chunks()
        elif segment == 'sentence':
            return semcor.sents()
        elif segment == 'chunk_sentence':
            return semcor.chunk_sents()
        elif segment == 'tagged_chunk':
            return list(map(str, semcor.tagged_chunks(tag='both')[:3]))
        elif segment == 'tagged_sentence':
            return [[str(chunk) for chunk in sent] for sent in semcor.tagged_sents(tag='both')[:2]]
        else:
            return None    

    def _download(self):
        import nltk
        nltk.download('semcor')



#####################################################
##
## THROWAWAY TEST CODE
##

def download_nltk_data():
    import nltk
    nltk.download()


# Semcor  = NLTKSemcorSource()
# Reader = Semcor.read(segment='word') 
# Reader = Semcor.read(segment='chunk') 
# Reader = Semcor.read(segment='sentence') 
# Reader = Semcor.read(segment='chunk_sentence') 
# Reader = Semcor.read(segment='tagged_chunk') 
# Reader = Semcor.read(segment='tagged_sentence') 

# print (Reader)


# import os

# dir_fd = os.open('somedir', os.O_RDONLY)
