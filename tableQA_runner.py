import glob
import os
import random
import sys
import gzip
import pickle

import argparse
import numpy as np

from config import BabiConfig, BabiConfigJoint
from train_test import train, train_linear_start, test
from util import parse_babi_task, build_model

import fasttext

seed_val = 42
random.seed(seed_val)
np.random.seed(seed_val)  # for reproducing

# EMBEDDINGS_MODEL_PATH = '../fastText/result/fil9.bin'


def run_tableQA(data_path, model_file):
    """
    Train and test for table QA
    """

    # Parse data
    train_files = glob.glob(data_path.format('train'))
    test_files  = glob.glob(data_path.format('test'))
    # SV: init dict with pre-trained vectors, e.g. from fastText
    # dictionary = fasttext.load_model(EMBEDDINGS_MODEL_PATH)
    dictionary = {"nil": 0}
    train_story, train_questions, train_qstory = parse_babi_task(train_files, dictionary, False)
    test_story, test_questions, test_qstory    = parse_babi_task(test_files, dictionary, False)
    # print test_questions
    print 'Dictionary:', len(dictionary)
    general_config = BabiConfig(train_story, train_questions, dictionary)

    memory, model, loss = build_model(general_config)

    if general_config.linear_start:
        train_linear_start(train_story, train_questions, train_qstory, memory, model, loss, general_config)
    else:
        train(train_story, train_questions, train_qstory, memory, model, loss, general_config)

    test(test_story, test_questions, test_qstory, memory, model, loss, general_config)

    # save_model
    with gzip.open(model_file, "wb") as f:
        print("Saving model to file %s ..." % model_file)
        reversed_dict = dict((ix, w) for w, ix in dictionary.items())
        pickle.dump((reversed_dict, memory, model, loss, general_config), f)


if __name__ == "__main__":
    dataset = 'sim'
    # test - small subset of synthetic data 
    # original MemN2N performance ::: train error: 0 | val error: 0 Test error: 0.000000
    # synth - larger set with synthetic data
    # sim - simulated data, generated using real table data but with artificially reduced domain variance
    # table - real table data extracted from a random open data csv file
    data_path = './data/%s_data_{}.txt' % dataset
    run_tableQA(data_path, './trained_model/memn2n_table_qa_model_%s.pklz' % dataset)
