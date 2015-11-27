#!/usr/bin/python3
#-*- coding: utf-8 -*-

from Tkinter import *
from urllib import urlopen, urlretrieve
from HTMLParser import HTMLParser
from PIL import Image, ImageTk
import urllib2

# simple web browser, Tk interface, nothing fancy

cache = []
home = ''
pictures = {}

class App(object):
	
	def __init__(self, master):
		
		toolbar = Frame(master)
		#toolbar
		self.e = Entry(toolbar)
		self.e.pack(side=LEFT)
		self.b = Button(toolbar, text='->', command=self.open_url)
		self.b.pack(side=LEFT)
		
		toolbar.pack(side=TOP)
		
		
		body = Frame(master)
		#scrollbar
		self.scrollbar = Scrollbar(body)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		
		#canvas
		self.canvas = Canvas(body, 
					width=600,
					height=800,
					yscrollcommand=self.scrollbar.set, 
					bg='white', 
					scrollregion=(0,0,1000,5000))
		
		self.canvas.pack(side=LEFT, fill=BOTH)
		self.scrollbar.config(command=self.canvas.yview)
		body.pack()
		
		#statusbar
		global statusbar
		statusbar = StatusBar(master)
		statusbar.pack(side=BOTTOM, fill=X)
		
	def open_url(self):
		image = Image.open('smiley.jpg')
		b = Picture(self.canvas, image, 0, 50)
		url = 'http://'+self.e.get()
		global home
		home = url
		goto(self.canvas, url)



def goto(canvas, url):
	global statusbar
	statusbar.set('%s' % url)
	global cache
	cache = []
	pictures = {}
	canvas.delete('all')
	data = urlopen(url).read().decode('utf-8')
	parser = MyHTMLParser()
	parser.feed(data)
	i=0

	while i < len(cache):
	
		if cache[i] == 'href':
			url = cache.pop(i+1)
			url = convert_url(url)
			name = cache.pop(i+1)
			#print(name, url)
			link = canvas.create_text(0,i*15,anchor=NW, text=name, fill='blue')
			link = Hyperlink(canvas, link, url) 

		elif cache[i] == 'src':
			url = cache.pop(i+1)
			url = convert_url(url)
			print 'hura', url
			download_image(url)
			image = Image.open('cache/%s' % getfilename(url))
			global pictures
			pictures[i] = Picture(canvas, image, 0, i*15)
			i += image.size[1] / 15
	
		else:
			canvas.create_text(0,i*15,anchor=NW, text=cache[i])
	
		i += 1 

	canvas.config(scrollregion=canvas.bbox(ALL))


def getfilename(url):
	return url.split('/')[-1]

def download_image(url):
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open('cache/%s' % file_name, 'wb')
	buffer = u.read()
	f.write(buffer)
	f.close()

def convert_url(url):
	global home
	if url.startswith('http'):
		return url
	else:
		return home+url
		
class Hyperlink(object):
	
	def __init__(self, canvas, itemid, link):
		self.tag = itemid
		self.canvas = canvas
		self.link = link
		self.canvas.tag_bind(self.tag, '<Button-1>', self.goto)
	
	def goto(self, event=None):
		print('Link: ', self.link)
		goto(self.canvas, self.link)
		
class Picture(object):
	
	def __init__(self, canvas, image, x, y):
		self.canvas = canvas
		self.image = image
		self.x = x
		self.y = y
		self.photo = ImageTk.PhotoImage(self.image)
		self.canvas.create_image(self.x,self.y, anchor=NW, image=self.photo)

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print('Start tag:', tag)
			
			#print('       attr:', attr)
		if tag == 'a':
			for attr in attrs:
				if 'href' in attr:
					cache.extend(attr)
			for attr in attrs:
				if 'src' in attr:
					cache.extend(attr)
		if tag == 'img':
			for attr in attrs:
				if 'src' in attr:
					cache.extend(attr)
				
						
			
	def handle_endtag(self,tag):
		print('End tag :', tag)
	def handle_data(self, data):
		cache.extend(data.splitlines())
		print('Data      :', data)
	def handle_comment(self, data):
		print('Comment   :', data)
	def handle_decl(self, data):
		print('Decl     :', data)
		
class StatusBar(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
		self.label.pack(fill=X)
		
	def set(self, format, *args):
		self.label.config(text=format % args)
		self.label.update_idletasks()
		
	def clear(self):
		self.label.config(text='')
		self.label.update_idletasks()
		
	
	

			
master = Tk()
gui = App(master)
master.mainloop()
