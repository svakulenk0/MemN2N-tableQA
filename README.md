## End-To-End Memory Networks for Question Answering on Tables




This is an implementation of MemN2N model in Python for the [bAbI question-answering tasks](http://fb.ai/babi) 
as shown in the Section 4 of the paper "[End-To-End Memory Networks](http://arxiv.org/abs/1503.08895)". It is based on 
Facebook's [Matlab code](https://github.com/facebook/MemNN/tree/master/MemN2N-babi-matlab).

![Web-based Demo](http://i.imgur.com/mKtZ7kB.gif)

## Requirements
* Python 2.7
* Numpy, Flask (only for web-based demo) can be installed via pip:
```
$ sudo pip install -r requirements.txt
```

## Usage
* To run use `babi_runner.py`

The output will look like:
```
Using data from data/tasks_1-20_v1-2/en
Train and test for task 1 ...
1 | train error: 0.876116 | val error: 0.75
|===================================               | 71% 0.5s
```


## Question Answering Demo
* In order to run the Web-based demo using the pretrained model `memn2n_model.pklz` in `trained_model/`, run:
```
python -m demo.qa
```

* Alternatively, you can try the console-based demo:
```
python -m demo.qa -console
```

* The pretrained model `memn2n_model.pklz` can be created by running:
```
python -m demo.qa -train
```

* To show all options, run `python -m demo.qa -h`


## Experiments

1. Synthetic patterns

* Data

Cell-based

1 Row1 City Klagenfurt
2 Row1 Immigration 19
3 Row1 Emmigration 10
4 Row2 City Feldkirch
5 Row2 Immigration 12
6 Row2 Emmigration 14
7 What is the Emmigration in Klagenfurt?	10	1 3

Vocab size: 29 unique words
Story max length: 18 words
Query max length: 7 words
Number of training samples: 10000
Number of test samples: 500

* Results

100 | train error: 0 | val error: 0
Test error: 0.000000
Finished in 21185.1s (MacAir)


2. Simulated data

Based on a real table (limiting vocabulary size and producing more training examples)

* Data

* Results

100 | train error: 0.0547153 | val error: 0.0917339
Test error: 0.058393


## Benchmarks
See the results [here](https://github.com/vinhkhuc/MemN2N-babi-python/tree/master/bechmarks).

### Acknowledgment
Based on [Vinh Khuc's implementation of MemN2N for babi tasks](https://github.com/vinhkhuc/MemN2N-babi-python).

### References
* Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus, 
  "[End-To-End Memory Networks](http://arxiv.org/abs/1503.08895)",
  *arXiv:1503.08895 [cs.NE]*.