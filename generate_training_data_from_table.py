#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 8, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

'''
import csv


DATA_DIR = './data/'
SAMPLE_CSV_FILE = 'OOE_Wanderungen_Zeitreihe.csv'
'''
Question templates are the tuples of the form: 
(natural language template for the question,
 column labels with the values to fill in the template,
 column label that contains answer to the question)
'''
QUESTION_TEMPLATES = [ 
                       ('What is the lau2 code for %s', ['lau2_name'], 'lau2_code'),
                       ('Which city has the lau2 code %s', ['lau2_code'], 'lau2_name'),
                       ('Which town has the lau2 code %s', ['lau2_code'], 'lau2_name'),
                       ('What was internal immigration in %s in %s', ['lau2_name', 'year'], 'internal_mig_immigration'),
                       ('What was international immigration in %s in %s', ['lau2_name', 'year'], 'international_mig_immigration'),
                       ('What was the total number of immigrants into %s for %s', ['lau2_name', 'year'], 'immigration_total'),
                       ('What was the number of emigrants from %s for %s internally', ['lau2_name', 'year'], 'internal_mig_emigration'),
                       ('What was the number of emigrants from %s for %s on the international level', ['lau2_name', 'year'], 'international_mig_emigration'),
                       ('What was the total number of emigrants from %s for %s on both internal and international levels', ['lau2_name', 'year'], 'emigration_total'),
                        ]


def load_csv(file_name):
    header = None
    rows = []
    with open(DATA_DIR+file_name, 'rb') as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if i == 0:
                header = line
            else:
                rows.append(line)
    return header, rows


def test_load_csv():
    header, rows = load_csv(SAMPLE_CSV_FILE)
    print header
    print rows[0]


def table2cells(file_name):
    header, rows = load_csv(SAMPLE_CSV_FILE)
    row_strs = []
    for i, row in enumerate(rows):
        cell_strs = []
        for j, cell in enumerate(row):
            cell_str = "%s %s" % (header[j], j)
            cell_strs.append(cell_str.lower().strip())
        row_strs.append(cell_strs)
    return row_strs


def test_table2cells():
    print table2cells(SAMPLE_CSV_FILE)[:2]


if __name__ == '__main__':
    test_table2cells()
