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

# EMBEDDINGS_MODEL_PATH = '../fastText/result/fil9.bin'
EMBEDDINGS_MODEL_PATH = 'embeddings/fil9.bin'
# print "Loading model from", EMBEDDINGS_MODEL_PATH
model = fasttext.load_model(EMBEDDINGS_MODEL_PATH)
# print "Finished loading"

print len(model.words) # number of words in dictionary
print model['king'] # get the vector of the word 'king'
print model['kingserwq'] # get the vector for an OOV word
