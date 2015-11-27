#!/usr/bin/python3
#-*- coding: utf-8 -*-

import operator
import random

class Card(object):
	rank_names = ['None', 'Ace', '2', '3', '4', '5', '6', '7', '8',
		'9', '10', 'Jack', 'Queen', 'King']
	suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
	def __init__(self, suit=0, rank=2):
		self.suit = suit
		self.rank = rank
	def __str__(self):
		return '%s of %s' % (Card.rank_names[self.rank],
							 Card.suit_names[self.suit])
							 
	def __lt__(self, other):
		t1 = self.suit, self.rank
		t2 = other.suit, other.rank
		if operator.eq(t1,t2):
			return 0
		elif operator.lt(t1,t2):
			return -1
		else:
			return 1

class Time(object):
	def __init__(self, hour=0, minutes=0, seconds=0):
		self.hour = hour
		self.minutes = minutes
		self.seconds = seconds
	def __str__(self):
		return '%.2d:%.2d:%.2d' % (self.hour, self.minutes, self.seconds)
	def __lt__(self, other):
		t1 = self.hour, self.minutes, self.seconds
		t2 = other.hour, other.minutes, other.seconds
		if operator.eq(t1,t2):
			return 0
		elif operator.lt(t1,t2):
			return -1
		else:
			return 1

class Deck(object):
	def __init__(self):
		self.cards = []
		for suit in range(4):
			for rank in range(1, 14):
				card = Card(suit, rank)
				self.cards.append(card)
	def __str__(self):
		res = []
		for card in self.cards:
			res.append(str(card))
		return '\n'.join(res)
	def pop_card(self):
		return self.cards.pop()
	def add_card(self, card):
		self.cards.append(card)
	def shuffle(self):
		random.shuffle(self.cards)
	def sort(self):
		res = []
		temp = []
		for card in self.cards:
			res.append((card.suit, card.rank))
		res.sort()
		for card in res:
			temp.append(Card(card[0],card[1]))
		self.cards = temp
	def move_cards(self, hand, n):
		for i in range(n):
			hand.add_card(self.pop_card())
	def deal_hands(self, n_hands, cards_per_hand):
		res = []
		for n in range(n_hands):
			handz = Hand(label=n)
			self.move_cards(handz, cards_per_hand)
			res.append(handz)
		return res
		
class Hand(Deck):
	def __init__(self, label=''):
		self.cards = []
		self.label = label
		
card1 = Card(rank=11, suit=1)
card2 = Card(rank=13, suit=1)
#print(operator.lt(card1,card2))

h1 = Time(4,46)
h2 = Time(4,46)
#print(h1, h2, operator.lt(h1,h2))

deck = Deck()
card = deck.pop_card()
handz = Hand('new hand')
r = deck.deal_hands(4, 3)
print(type(handz).mro())
"""
for hand in r:
	print(hand.label)
	print(hand)
"""
