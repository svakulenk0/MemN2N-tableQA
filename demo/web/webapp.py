"""
Web-based demo
"""
import glob
import flask
import numpy as np

from demo.qa import MemN2N
from util import parse_babi_task

app = flask.Flask(__name__)
memn2n = None
test_story, test_questions, test_qstory = None, None, None


def init(data_dir, model_file):
    """ Initialize web app """
    global memn2n, test_story, test_questions, test_qstory

    # Try to load model
    memn2n = MemN2N(data_dir, model_file)
    memn2n.load_model()

    # SV create word vectors for all the dictionary words
    print("Embedding dictionary words")
    for word in memn2n.general_config.dictionary.keys():
        # SV assign vector to each word in the dictionary
        memn2n.dict_vectors[word] = memn2n.word_model[word]

    # Read test data
    # test_data_path = glob.glob('%s/qa*_*_test.txt' % memn2n.data_dir)
    test_data_path  = glob.glob(memn2n.data_path.format('test'))
    # load different dataset with samples, e.g. real table data
    # test_data_path  = glob.glob('./data/table_data_{}.txt'.format('test'))
    print("Reading test data from %s ..." % test_data_path)

    # test_story, test_questions, test_qstory = \
    #     parse_babi_task(test_data_path, memn2n.general_config.dictionary, False)
    # update dictionary with new words
    test_story, test_questions, test_qstory = \
        memn2n.parse_babi_task(test_data_path, False)
    
    # SV expand reversed_dict with test data
    print len(memn2n.general_config.dictionary)
    # Get reversed dictionary mapping index to word
    memn2n.reversed_dict = dict((ix, w) for w, ix in memn2n.general_config.dictionary.items())


def run():
    app.run()


@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route('/get/story', methods=['GET'])
def get_story():
    question_idx      = np.random.randint(test_questions.shape[1])
    story_idx         = test_questions[0, question_idx]
    last_sentence_idx = test_questions[1, question_idx]
    # print test_questions
    print question_idx, story_idx, last_sentence_idx

    story_txt, question_txt, correct_answer = memn2n.get_story_texts(test_story, test_questions, test_qstory,
                                                                     question_idx, story_idx, last_sentence_idx)
    print story_txt
    # Format text
    story_txt = "\n".join(story_txt)
    question_txt += "?"

    return flask.jsonify({
        "question_idx": question_idx,
        "story": story_txt,
        "question": question_txt,
        "correct_answer": correct_answer
    })


@app.route('/get/answer', methods=['GET'])
def get_answer():
    question_idx  = int(flask.request.args.get('question_idx'))
    user_question = flask.request.args.get('user_question', '')

    story_idx         = test_questions[0, question_idx]
    last_sentence_idx = test_questions[1, question_idx]

    pred_answer_idx, pred_prob, memory_probs, dis_question = memn2n.predict_answer(test_story, test_questions, test_qstory,
                                                                     question_idx, story_idx, last_sentence_idx,
                                                                     user_question)
    pred_answer = memn2n.reversed_dict[pred_answer_idx]
    print dis_question
    return flask.jsonify({
        # disumbiguated question
        "dis_question" : "<br>".join(dis_question),
        "pred_answer" : pred_answer,
        "pred_prob" : pred_prob,
        "memory_probs": memory_probs.T.tolist()
    })
