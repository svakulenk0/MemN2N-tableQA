#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 8, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

'''
import csv


DATA_DIR = './'
SAMPLE_CSV_FILE = 'OOE_Wanderungen_Zeitreihe.csv'


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
            cell_str = "%s %s" % (header[j], cell)
            cell_strs.append(cell_str.lower().strip())
        row_strs.append(cell_strs)
    return row_strs


def test_table2cells():
    print table2cells(SAMPLE_CSV_FILE)[:2]


if __name__ == '__main__':
    test_table2cells()
