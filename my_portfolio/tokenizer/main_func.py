import pandas as  pd
import numpy as np
import pickle
import sys
from tokenizer import randomforest
sys.modules['randomforest'] = randomforest

def sort(dict):
	return sorted(dict.items(), key=lambda x:x[1], reverse=True)

def sort_key(d, subject_key):
	return sorted(d, key=lambda x:x[subject_key], reverse=True)

def average(l):
	return sum(l)/len(l)

def variance(l, avg):
	l2 = (np.array(l)-avg)**2
	vari = np.sum(l2)
	return vari

def dict_update(d, key, value):
	if not key in d.keys():
		d[key] = 0
	d[key] += value
	return d

def dicts_update(d1, d2):
	d3 = dict_init(list(d1.keys())+list(d2.keys()))
	for key in d1.keys():
		d3[key] += filter_dict_sum(d1, key)
	for key in d2.keys():
		d3[key] += filter_dict_sum(d2, key)
	return d3

#dictの初期化
def dict_init(l):
	zeros = [0 for _ in range(len(l))]
	return dict(zip(l, zeros))

def dict_init_l(l):
	zeros = [[] for _ in range(len(l))]
	return dict(zip(l, zeros))

def dict_add(d, labels, l):
	for key, value in zip(labels, l):
		d[key] += [value]
	return d

#dictの総和
def dict_sum(d):
	s = sum(d.values())
	if s == 0:
		return 0
	return s

#dはdict、kは0がkeyで1がvalue、vはフィルタリング項目
def filter_key(d, k):
	return dict(filter(lambda x: k in x[0], d.items()))

def filter_value_equal(d, v):
	return dict(filter(lambda x: x[1] == v, d.items()))
def filter_value_or_more(d, v):
	return dict(filter(lambda x: x[1] >= v, d.items()))
def filter_value_or_less(d, v):
	return dict(filter(lambda x: x[1] <= v, d.items()))

#フィルターしたkeyのリスト
def filter_dict_len(d, v, ctr="equal"):
	if ctr == "equal":
		return len(filter_value_equal(d, v))
	elif ctr == "or_more":
		return len(filter_value_or_more(d, v))
	elif ctr == "or_less":
		return len(filter_value_or_less(d, v))

#フィルターしたvalueの総和
def filter_dict_sum(d, k):
	return dict_sum(filter_key(d, k))
	
def estimate(model_name, data_x):
	filename = './tokenizer/{}_model.sav'.format(model_name)
	loaded_model = pickle.load(open(filename, 'rb'))
	result = loaded_model.predict(data_x)
	return result

