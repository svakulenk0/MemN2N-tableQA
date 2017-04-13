## End-To-End Memory Networks for Question Answering on Tables



## Requirements
* Python 2.7
* Numpy, Flask (only for web-based demo) can be installed via pip:
```
$ sudo pip install -r requirements.txt
```

## Usage

* Load fastText embeddings

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

1. Synthetic patterns (synth)

* Data

Cell-based babi-like data format.

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

also on smaller dataset!
Finished in 57.6s (MacAir)

2. Simulated data (sim)

Based on a real table (limiting vocabulary size and producing more training examples)

* Data

1 Row1 NUTS2 AT31
2 Row1 LAU2_CODE 41004
3 Row1 LAU2_NAME Allhaming
4 Row1 YEAR 2002
5 Row1 INTERNAL_MIG_IMMIGRATION 2
6 Row1 INTERNATIONAL_MIG_IMMIGRATION 4
7 Row1 IMMIGRATION_TOTAL 1
8 Row1 INTERNAL_MIG_EMIGRATION 3
9 Row1 INTERNATIONAL_MIG_EMIGRATION 4
10 Row1 EMIGRATION_TOTAL 3
11 Row2 NUTS2 AT31
12 Row2 LAU2_CODE 41003
13 Row2 LAU2_NAME Geretsberg
14 Row2 YEAR 2005
15 Row2 INTERNAL_MIG_IMMIGRATION 2
16 Row2 INTERNATIONAL_MIG_IMMIGRATION 2
17 Row2 IMMIGRATION_TOTAL 10240
18 Row2 INTERNAL_MIG_EMIGRATION 6
19 Row2 INTERNATIONAL_MIG_EMIGRATION 1
20 Row2 EMIGRATION_TOTAL 6
21 What is the INTERNAL_MIG_IMMIGRATION for Geretsberg?	2	13 15

* Results

100 | train error: 0.0547153 | val error: 0.0917339
Test error: 0.087500

3. Real data (table)

Sample CSV table transformed into babi-format.

* Data

1 Row1 NUTS2 AT31
2 Row1 LAU2_CODE 41819
3 Row1 LAU2_NAME Sipbachzell
4 Row1 YEAR 2002
5 Row1 INTERNAL_MIG_IMMIGRATION 57
6 Row1 INTERNATIONAL_MIG_IMMIGRATION 14
7 Row1 IMMIGRATION_TOTAL 71
8 Row1 INTERNAL_MIG_EMIGRATION 61
9 Row1 INTERNATIONAL_MIG_EMIGRATION 11
10 Row1 EMIGRATION_TOTAL 72
11 Row2 NUTS2 AT31
12 Row2 LAU2_CODE 41820
13 Row2 LAU2_NAME Stadl-Paura
14 Row2 YEAR 2002
15 Row2 INTERNAL_MIG_IMMIGRATION 216
16 Row2 INTERNATIONAL_MIG_IMMIGRATION 57
17 Row2 IMMIGRATION_TOTAL 273
18 Row2 INTERNAL_MIG_EMIGRATION 219
19 Row2 INTERNATIONAL_MIG_EMIGRATION 41
20 Row2 EMIGRATION_TOTAL 260
21 Row3 NUTS2 AT31
22 Row3 LAU2_CODE 41821
23 Row3 LAU2_NAME Steinerkirchen an der Traun
24 Row3 YEAR 2002
25 Row3 INTERNAL_MIG_IMMIGRATION 82
26 Row3 INTERNATIONAL_MIG_IMMIGRATION 11
27 Row3 IMMIGRATION_TOTAL 93
28 Row3 INTERNAL_MIG_EMIGRATION 74
29 Row3 INTERNATIONAL_MIG_EMIGRATION 17
30 Row3 EMIGRATION_TOTAL 91
31 Row4 NUTS2 AT31
32 Row4 LAU2_CODE 41822
33 Row4 LAU2_NAME Steinhaus
34 Row4 YEAR 2002
35 Row4 INTERNAL_MIG_IMMIGRATION 42
36 Row4 INTERNATIONAL_MIG_IMMIGRATION 10
37 Row4 IMMIGRATION_TOTAL 52
38 Row4 INTERNAL_MIG_EMIGRATION 48
39 Row4 INTERNATIONAL_MIG_EMIGRATION 7
40 Row4 EMIGRATION_TOTAL 55
41 What is the INTERNATIONAL_MIG_IMMIGRATION for Steinhaus?	10	33 36

* Results

Row-based formatting does not work error ~ 1

Cell-based formatting:

100 | train error: 0.148849 | val error: 0.535156               
Test error: 0.189338

### Acknowledgment

* Based on [Vinh Khuc: MemN2N for babi tasks](https://github.com/vinhkhuc/MemN2N-babi-python).
* [YerevaNN: Dynamic-memory-networks-in-Theano](https://github.com/YerevaNN/Dynamic-memory-networks-in-Theano)

### References
* Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus, 
  [End-To-End Memory Networks](http://arxiv.org/abs/1503.08895)
* Kumar et al. [Dynamic memory networks](http://arxiv.org/abs/1506.07285)