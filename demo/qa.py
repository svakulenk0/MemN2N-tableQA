"""
Demo of using Memory Network for question answering
"""
import glob
import os
import gzip
import sys
import pickle

import argparse
import numpy as np

# SV
import fasttext
from sklearn.metrics.pairwise import cosine_similarity

from config import BabiConfigJoint
from train_test import train, train_linear_start
from util import parse_babi_task, build_model, NWORDS, NSTORIES, NSENTENCES

# EMBEDDINGS_MODEL_PATH = '../fastText/result/fil9.bin'
EMBEDDINGS_MODEL_PATH = 'embeddings/fil9.bin'


class MemN2N(object):
    """
    MemN2N class
    """
    def __init__(self, data_dir, model_file, dataset='sim'):
        # specify pre-trained models to load in the interface
        # and the sample dataset for evaluation: test sim synth table
        self.data_dir       = data_dir
        self.data_path      = './data/%s_data_{}.txt' % dataset
        self.model_file     = './trained_model/memn2n_table_qa_model_%s.pklz' % dataset
        # self.model_file     = model_file
        self.reversed_dict  = None
        self.memory         = None
        self.model          = None
        self.loss           = None
        self.general_config = None
        # SV load model to embed OOV words
        print("Loading word embeddings model")
        self.word_model = fasttext.load_model(EMBEDDINGS_MODEL_PATH)
        # SV keep word vectors for all the dictionary words
        self.dict_vectors = {}


    def save_model(self):
        with gzip.open(self.model_file, "wb") as f:
            print("Saving model to file %s ..." % self.model_file)
            pickle.dump((self.reversed_dict, self.memory, self.model, self.loss, self.general_config), f)

    def load_model(self):
        # Check if model was loaded
        if self.reversed_dict is None or self.memory is None or \
                self.model is None or self.loss is None or self.general_config is None:
            print("Loading MemNN-QA model from file %s ..." % self.model_file)
            with gzip.open(self.model_file, "rb") as f:
                self.reversed_dict, self.memory, self.model, self.loss, self.general_config = pickle.load(f)

    def train(self):
        """
        Train MemN2N model using training data for tasks.
        """
        np.random.seed(42)  # for reproducing
        # assert self.data_dir is not None, "data_dir is not specified."
        # print("Reading data from %s ..." % self.data_dir)

        # Parse data
        train_data_path = glob.glob(self.data_path.format('train'))
        test_data_path  = glob.glob(self.data_path.format('test'))
        
        # Parse training data
        # train_data_path = glob.glob('%s/qa*_*_train.txt' % self.data_dir)
        # init dict with pre-trained vectors, e.g. from fastText
        dictionary = {"nil": 0}
        train_story, train_questions, train_qstory = parse_babi_task(train_data_path, dictionary, False)

        # Parse test data just to expand the dictionary so that it covers all words in the test data too
        # test_data_path = glob.glob('%s/qa*_*_test.txt' % self.data_dir)
        parse_babi_task(test_data_path, dictionary, False)

        # Get reversed dictionary mapping index to word
        self.reversed_dict = dict((ix, w) for w, ix in dictionary.items())

        # Construct model
        self.general_config = BabiConfigJoint(train_story, train_questions, dictionary)
        self.memory, self.model, self.loss = build_model(self.general_config)

        # Train model
        if self.general_config.linear_start:
            train_linear_start(train_story, train_questions, train_qstory,
                               self.memory, self.model, self.loss, self.general_config)
        else:
            train(train_story, train_questions, train_qstory,
                  self.memory, self.model, self.loss, self.general_config)

        # Save model
        self.save_model()

    def parse_babi_task(self, data_files, include_question):
        """ Parse bAbI data. And expand the dictionary.

        Args:
           data_files (list): a list of data file's paths.
           dictionary (dict): word's dictionary
           include_question (bool): whether count question toward input sentence.

        Returns:
            A tuple of (story, questions, qstory):
                story (3-D array)
                    [position of word in sentence, sentence index, story index] = index of word in dictionary
                questions (2-D array)
                    [0-9, question index], in which the first component is encoded as follows:
                        0 - story index
                        1 - index of the last sentence before the question
                        2 - index of the answer word in dictionary
                        3 to 13 - indices of supporting sentence
                        14 - line index
                qstory (2-D array) question's indices within a story
                    [index of word in question, question index] = index of word in dictionary
        """
        # Try to reserve spaces beforehand (large matrices for both 1k and 10k data sets)
        story     = np.zeros((NWORDS, NSENTENCES, len(data_files) * NSTORIES), np.int16)
        questions = np.zeros((14, len(data_files) * 10000), np.int16)
        qstory    = np.zeros((NWORDS, len(data_files) * 10000), np.int16)

        # NOTE: question's indices are not reset when going through a new story
        story_idx, question_idx, sentence_idx, max_words, max_sentences = -1, -1, -1, 0, 0

        # Mapping line number (within a story) to sentence's index (to support the flag include_question)
        mapping = None

        for fp in data_files:
            with open(fp) as f:
                for line_idx, line in enumerate(f):
                    line = line.rstrip().lower()
                    words = line.split()
                    # Story begins
                    if words[0] == '1':
                        story_idx += 1
                        sentence_idx = -1
                        mapping = []

                    # FIXME: This condition makes the code more fragile!
                    if '?' not in line:
                        is_question = False
                        sentence_idx += 1
                    else:
                        is_question = True
                        question_idx += 1
                        questions[0, question_idx] = story_idx
                        questions[1, question_idx] = sentence_idx
                        if include_question:
                            sentence_idx += 1

                    mapping.append(sentence_idx)

                    # Skip substory index
                    for k in range(1, len(words)):
                        w = words[k]

                        if w.endswith('.') or w.endswith('?'):
                            w = w[:-1]
                        if w not in self.general_config.dictionary:
                            self.general_config.dictionary[w] = len(self.general_config.dictionary)

                        if max_words < k:
                            max_words = k
                        # print sentence_idx, story_idx
                        if not is_question:
                            # look up word in a dictionary
                            story[k - 1, sentence_idx, story_idx] = self.general_config.dictionary[w]
                        else:
                            qstory[k - 1, question_idx] = self.general_config.dictionary[w]
                            if include_question:
                                story[k - 1, sentence_idx, story_idx] = self.general_config.dictionary[w]

                            # NOTE: Punctuation is already removed from w
                            if words[k].endswith('?'):
                                answer = words[k + 1]
                                if answer not in self.general_config.dictionary:
                                    self.general_config.dictionary[answer] = len(self.general_config.dictionary)

                                questions[2, question_idx] = self.general_config.dictionary[answer]

                                # Indices of supporting sentences
                                for h in range(k + 2, len(words)):
                                    questions[1 + h - k, question_idx] = mapping[int(words[h]) - 1]

                                questions[-1, question_idx] = line_idx
                                break

                    if max_sentences < sentence_idx + 1:
                        max_sentences = sentence_idx + 1


        story     = story[:max_words, :max_sentences, :(story_idx + 1)]
        questions = questions[:, :(question_idx + 1)]
        qstory    = qstory[:max_words, :(question_idx + 1)]
        print questions[1, 0]
        return story, questions, qstory

    def get_story_texts(self, test_story, test_questions, test_qstory,
                        question_idx, story_idx, last_sentence_idx):
        """
        Get text of question, its corresponding fact statements.
        """
        train_config = self.general_config.train_config
        enable_time = self.general_config.enable_time
        max_words = train_config["max_words"] \
            if not enable_time else train_config["max_words"] - 1
        story = [[self.reversed_dict[test_story[word_pos, sent_idx, story_idx]]
                  for word_pos in range(max_words)]
                  for sent_idx in range(last_sentence_idx + 1)]
        # print story
        question = [self.reversed_dict[test_qstory[word_pos, question_idx]]
                    for word_pos in range(max_words)]

        story_txt = [" ".join([w.decode('latin-1') for w in sent if w != "nil"]) for sent in story]
        question_txt = " ".join([w.decode('latin-1') for w in question if w != "nil"])
        correct_answer = self.reversed_dict[test_questions[2, question_idx]].decode('latin-1')

        return story_txt, question_txt, correct_answer

    def predict_answer(self, test_story, test_questions, test_qstory,
                       question_idx, story_idx, last_sentence_idx,
                       user_question=''):
        # Get configuration
        nhops        = self.general_config.nhops
        train_config = self.general_config.train_config
        batch_size   = self.general_config.batch_size
        dictionary   = self.general_config.dictionary
        enable_time  = self.general_config.enable_time

        max_words = train_config["max_words"] \
            if not enable_time else train_config["max_words"] - 1

        input_data = np.zeros((max_words, batch_size), np.float32)
        # init with 0
        input_data[:] = dictionary["nil"]
        self.memory[0].data[:] = dictionary["nil"]

        # Check if user provides questions and it's different from suggested question
        _, suggested_question, _ = self.get_story_texts(test_story, test_questions, test_qstory,
                                                        question_idx, story_idx, last_sentence_idx)
        user_question_provided = user_question != '' and user_question != suggested_question
        encoded_user_question = None
        dis_question = []
        # new question different from test data
        if user_question_provided:
            # TODO seq2seq translation/projection model
            
            # print("User question = '%s'" % user_question)
            user_question = user_question.strip()
            if user_question[-1] == '?':
                user_question = user_question[:-1]
            qwords = user_question.rstrip().lower().split() # skip '?'

            # Encoding
            encoded_user_question = np.zeros(max_words)
            encoded_user_question[:] = dictionary["nil"]
            for ix, w in enumerate(qwords):
                if w in dictionary:
                    encoded_user_question[ix] = dictionary[w]
                else:
                    print("WARNING - The word '%s' is not in dictionary." % w)
                    # SV deal with OOV words!
                    # look it up in fasttext
                    word_vector = self.word_model[w]
                    print 'fastText embedding:', word_vector
                    # resolve it with one of the vocabulary words
                    # iterate over and compare vector with each word in the dictionary
                    # init nn search
                    # TODO optimize cosine_similarity comparison on a matrix
                    nn = None
                    max_cosine = 0
                    for word, dict_vector in self.dict_vectors.items():
                        cosine = cosine_similarity(word_vector, dict_vector)[0][0]
                        if cosine > max_cosine:
                            nn = word
                            max_cosine = cosine
                    if max_cosine > 0.6:
                        encoded_user_question[ix] = dictionary[nn]
                        # print w + ' recognized as ' + nn
                        dis_question.append(w.decode('latin-1') + ' recognized as ' + nn.decode('latin-1') + ' ' + "%.2f" % max_cosine)
                        # dis_question.append(w + ' recognized as ' + nn)
                    else:
                        dis_question.append(w.decode('latin-1') + ' is not recognized and ignored')

        # Input data and data for the 1st memory cell
        # Here we duplicate input_data to fill the whole batch
        for b in range(batch_size):
            d = test_story[:, :(1 + last_sentence_idx), story_idx]

            offset = max(0, d.shape[1] - train_config["sz"])
            d = d[:, offset:]

            self.memory[0].data[:d.shape[0], :d.shape[1], b] = d

            if enable_time:
                self.memory[0].data[-1, :d.shape[1], b] = \
                    np.arange(d.shape[1])[::-1] + len(dictionary) # time words

            if user_question_provided:
                input_data[:test_qstory.shape[0], b] = encoded_user_question
            else:
                input_data[:test_qstory.shape[0], b] = test_qstory[:, question_idx]

        # Data for the rest memory cells
        for i in range(1, nhops):
            self.memory[i].data = self.memory[0].data

        # Run model to predict answer
        out = self.model.fprop(input_data)
        memory_probs = np.array([self.memory[i].probs[:(last_sentence_idx + 1), 0] for i in range(nhops)])

        # Get answer for the 1st question since all are the same
        pred_answer_idx  = out[:, 0].argmax()
        pred_prob = out[pred_answer_idx, 0]

        return pred_answer_idx, pred_prob, memory_probs, dis_question


def train_model(data_dir, model_file):
    memn2n = MemN2N(data_dir, model_file)
    memn2n.train()


def run_console_demo(data_dir, model_file):
    """
    Console-based demo
    """
    memn2n = MemN2N(data_dir, model_file)

    # Try to load model
    memn2n.load_model()

    # Read test data
    # test_data_path = glob.glob('%s/qa*_*_test.txt' % memn2n.data_dir)
    test_data_path  = glob.glob(memn2n.data_path.format('test'))
    # load different dataset with samples
    # test_data_path  = glob.glob('./data/table_data_{}.txt'.format('test'))
    print("Reading test data from %s ..." % test_data_path)

    # print len(memn2n.general_config.dictionary)

    
    test_story, test_questions, test_qstory = \
        memn2n.parse_babi_task(test_data_path, False)
    
    # SV expand reversed_dict with test data
    # print len(memn2n.general_config.dictionary)
    # Get reversed dictionary mapping index to word
    memn2n.reversed_dict = dict((ix, w) for w, ix in memn2n.general_config.dictionary.items())

    while True:
        # Pick a random question
        question_idx      = np.random.randint(test_questions.shape[1])
        story_idx         = test_questions[0, question_idx]
        last_sentence_idx = test_questions[1, question_idx]

        # Get story and question
        story_txt, question_txt, correct_answer = memn2n.get_story_texts(test_story, test_questions, test_qstory,
                                                                         question_idx, story_idx, last_sentence_idx)
        print("* Story:")
        print("\n\t".join(story_txt))
        print("\n* Suggested question:\n\t%s?" % question_txt)

        while True:
            user_question = raw_input("Your question (press Enter to use the suggested question):\n\t")

            pred_answer_idx, pred_prob, memory_probs = \
                memn2n.predict_answer(test_story, test_questions, test_qstory,
                                      question_idx, story_idx, last_sentence_idx,
                                      user_question)

            pred_answer = memn2n.reversed_dict[pred_answer_idx]

            print("* Answer: '%s', confidence score = %.2f%%" % (pred_answer, 100. * pred_prob))
            if user_question == '':
                if pred_answer == correct_answer:
                    print("  Correct!")
                else:
                    print("  Wrong. The correct answer is '%s'" % correct_answer)

            print("\n* Explanation:")
            print("\t".join(["Memory %d" % (i + 1) for i in range(len(memory_probs))]) + "\tText")
            for sent_idx, sent_txt in enumerate(story_txt):
                prob_output = "\t".join(["%.3f" % mem_prob for mem_prob in memory_probs[:, sent_idx]])
                print("%s\t%s" % (prob_output, sent_txt))

            asking_another_question = raw_input("\nDo you want to ask another question? [y/N] ")
            if asking_another_question == '' or asking_another_question.lower() == 'n': break

        will_continue = raw_input("Do you want to continue? [Y/n] ")
        if will_continue != '' and will_continue.lower() != 'y': break
        print("=" * 70)


def run_web_demo(data_dir, model_file):
    from demo.web import webapp
    webapp.init(data_dir, model_file)
    webapp.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-dir", default="data/tasks_1-20_v1-2/en",
                        help="path to dataset directory (default: %(default)s)")
    # parser.add_argument("-m", "--model-file", default="trained_model/memn2n_model.pklz",
    parser.add_argument("-m", "--model-file", default="trained_model/memn2n_table_qa_model.pklz",
                        help="model file (default: %(default)s)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-train", "--train", action="store_true",
                       help="train model (default: %(default)s)")
    group.add_argument("-console", "--console-demo", action="store_true",
                       help="run console-based demo (default: %(default)s)")
    group.add_argument("-web", "--web-demo", action="store_true", default=True,
                       help="run web-based demo (default: %(default)s)")
    args = parser.parse_args()

    # if not os.path.exists(args.data_dir):
    #     print("The data directory '%s' does not exist. Please download it first." % args.data_dir)
    #     sys.exit(1)

    if args.train:
        train_model(args.data_dir, args.model_file)
    elif args.console_demo:
        run_console_demo(args.data_dir, args.model_file)
    else:
        run_web_demo(args.data_dir, args.model_file)
