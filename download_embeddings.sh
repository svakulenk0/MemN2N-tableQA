#!/usr/bin/env bash
#
# Created on Apr 13, 2017

# .. codeauthor: svitlana vakulenko
    # <svitlana.vakulenko@gmail.com>

# Acknowledgements: 
# fastText

# Downloads the fastText model pre-trained on English Wikipedia

EMBEDDINGSDIR=embeddings

mkdir -p "${EMBEDDINGSDIR}"

wget -c http://mattmahoney.net/dc/enwik9.zip -P "${EMBEDDINGSDIR}"
unzip "${EMBEDDINGSDIR}/enwik9.zip" -d "${EMBEDDINGSDIR}"