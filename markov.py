#!/usr/bin/python3
#-*- coding: utf-8 -*-


import string
import random
import bisect
import sys

def markov(t, ahead=2):
	d = {}
	i = 0
	while i < len(t) - ahead:
		item = t[i]
		#d.setdefault(item, []).append(t[i+1:i+1+ahead])
		d.setdefault(tuple(t[i:i+ahead]), []). append(t[i+ahead])
		i += 1
	for key, value in d.items():
		d[key] = make_histogram(value)
	return d
	
def make_histogram(t):
	d = {}
	for item in t:
		if type(item) == list:
			item = tuple(item)
		d[(item)] = d.setdefault((item), 0) + 1
	return d
		
def skip_headlines(fin, stop = '*'):
	for line in fin:
		if line.startswith(stop):
			break
			
def filtr_line(line):
	t = []
	for word in line.split():
		for letter in word:
			if letter in string.whitespace:
				word = word.replace(letter, '')
		#word = word.lower()
		t.append(word)
	return t
	
def table_file(filename, skip=False):
	t = []
	fin = open(filename)
	if skip:
		skip_headlines(fin)
	for line in fin:
		for word in filtr_line(line):
			t.append(word)
	return t

def cumult(t):
	i = 0
	while i < len(t) - 1:
		t[i+1] += t[i] 
		i += 1
	return t

def choose_from_hist(hist):
	t = []
	keys = []
	for key in hist:
		t.append(hist[key])
		keys.append(key)
	t = cumult(t)
	r = random.randint(1,t[len(t)-1])
	index = bisect.bisect_left(t, r)
	return keys[index]
	
def alter_tuple(t, word):
	return t[1:]+(word,)
	
		
def go(filename, n, l):
	t = table_file(filename)
	d = make_histogram(t)
	mar = markov(t, n)
	base = random.choice(list(mar.keys()))
	s = ''
	for i in range(int(l/2)):
		
		ahead = choose_from_hist(mar[base])
		s += ' ' + ahead
		base = alter_tuple(base, ahead)
	print(s)	
	
def main(name, filename='mashup.txt', n = 2, l=100):
	try:
		l = int(l)
		n = int(n)
	except:
		print('Usage: markov.py filename [# of words] [prefix length]')
	else:
		go(filename, n, l)

if __name__ == '__main__':
	main(*sys.argv)
