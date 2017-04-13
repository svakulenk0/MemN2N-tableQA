#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 09, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Acknowledgements: 
* fastText https://pypi.python.org/pypi/fasttext

Test scripts for Python port of FastText
'''

import fasttext

EMBEDDINGS_MODEL = 'fil9.bin'
print "Loading", EMBEDDINGS_MODEL
model = fasttext.load_model('./embeddings/'+EMBEDDINGS_MODEL)
print "Finished loading"

print len(model.words) # number of words in dictionary
print model['king'] # get the vector of the word 'king'
print model['kingserwq'] # get the vector for an OOV word
