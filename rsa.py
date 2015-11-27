#!/usr/bin/python3
#-*- coding: utf-8 -*-

import random

def is_prime_number(n):
	i = 2
	while i <= (n**(0.5) + 1):
		if n%i == 0:
			return False
		i+=1
	return True

def generate_prime_number(start, stop):
	while start <= stop:
		if is_prime_number(start):
			return start
		start+=1

def gcd(a, b):
	if a == b:
		return a
	if a > b:
		return gcd(a - b, b)
	if b > a:
		return gcd(a, b - a)
		
def public_key(totient):
	while True:
		x = random.randint(2, totient - 1)
		if gcd(totient, x) == 1:
			return x
	print('Erorr: Cant generate public-key')
		
def extended_euklides(a, b):
	u = 1
	w = a
	x = 0
	z = b
	while w:
		if w < z:
			q = u
			u = x
			x = q
			q = w
			w = z
			z = q
		q =int(w / z)
		u = u - (q * x)
		w = w - (q * z)
	if z == 1:
		if x < 0:
			x+=b
			return x
	else:
		return False
	
def generate_key(p, q):
	global n, e, d, totient
	while d == None:
		n = p * q 
		totient = (p - 1) * (q - 1)
		e = public_key(totient)
		d = extended_euklides(e, totient)
	
	# public key = (e, n)
	# private key = (d, n)

def encryption(e, n, t):
	if t > 0 and t < n:
		return (t**e)%n

def decryption(d, n, c):
	if c > 0 and c < n:
		return (c**d)%n

def encrypt_msg(string):
	c = []
	for i in string:
		c.append(encryption(e, n, ord(i)))
	print('Enrypted msg = ', c)
	return c
	
def decrypt_msg(t):
	temp = ''
	for i in t:
		temp += chr(decryption(d, n, i))
	print('Decrypted msg = ', temp)
		
d = None
p = generate_prime_number(10, 500)
q = generate_prime_number(501, 90000)
generate_key(p, q)
print('p = ', p)
print('q = ', q)
print('n = ', n)
print('totient = ', totient)
print('e = ', e)
print('d = ', d)


msg = input()
c = encrypt_msg(msg)
decrypt_msg(c)
#c = encryption(e, n, ord('h'))
#m = decryption(d, n, c)	


