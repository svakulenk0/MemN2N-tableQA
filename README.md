## End-To-End Memory Networks for Question Answering on Tables



## Requirements
* Python 2.7
* Numpy, Flask (only for web-based demo) 
* fastText (+cython)

can be installed via pip:
```
$ sudo pip install -r requirements.txt
```

## Pre-requisite

1. Provide the correct path to the pre-trained fastText model (clone fastText Github repository and run ./word-vector-example.sh to train a model on the English Wikipedia) 
download pre-trained model
('make clean' and 'unzip enwik9.zip' before)

* To train and evaluate the model use `tableQA_runner.py`


## Question Answering Demo
* In order to run the Web-based demo using the pretrained model in `trained_model/`, run:
```
python -m demo.qa
```

* Alternatively, you can try the console-based demo:
```
python -m demo.qa -console
```

* The pretrained model can be created by running:
```
python -m demo.qa -train
```

* To show all options, run `python -m demo.qa -h`


## Experiments


### Data

Synthetic data based on a real table (limiting vocabulary size and producing more training examples)

Cell-based formatting

Dictionary: 65

1 Row1 LAU2_NAME Allhaming

2 Row1 YEAR 2002

3 Row1 INTERNAL_MIG_IMMIGRATION 2

4 Row1 INTERNATIONAL_MIG_IMMIGRATION 4

5 Row2 LAU2_NAME Geretsberg

6 Row2 YEAR 2005

7 Row2 INTERNAL_MIG_IMMIGRATION 3

8 Row2 INTERNATIONAL_MIG_IMMIGRATION 5

9 What is the INTERNAL_MIG_IMMIGRATION for Geretsberg?	3	5 7

### Settings

* linear start

* 2 question templates

* BOW


### Results


1. Simple key 

What is the EMIGRATION_TOTAL for Helfenberg?	2	13 20

IMMIGRATION_TOTAL in Burgkirchen?	4	3 7


Number of training examples 5949
9 | train error: 0 | val error: 0                              
Number of testing examples 3389
Test error: 0.000298


2. Complex key

What is the INTERNAL_MIG_IMMIGRATION for Grieskirchen in 2004?	4	13 14 15

IMMIGRATION_TOTAL in Burgkirchen for 2002?	10240	23 24 27


Number of training examples 18953
68 | train error: 0 | val error: 0                              
Number of testing examples 3941
Test error: 0.000762


## Acknowledgment

* Based on [Vinh Khuc: MemN2N for babi tasks](https://github.com/vinhkhuc/MemN2N-babi-python).
* Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus, 
  [End-To-End Memory Networks](http://arxiv.org/abs/1503.08895)

### Related Work
* [YerevaNN: Dynamic-memory-networks-in-Theano](https://github.com/YerevaNN/Dynamic-memory-networks-in-Theano)
* Kumar et al. [Dynamic memory networks](http://arxiv.org/abs/1506.07285)