#!/usr/bin/python
#-*- coding: utf-8 -*-

from Tkinter import *
import Image
import ImageTk

# simple drawing app
# choose shape to draw, input name of the color
# and make (contemporary) art

class Draggable(object):
	
	def __init__(self, canvas, itemid):
		self.tag = itemid
		self.canvas = canvas
		self.canvas.tag_bind(self.tag, '<Button-1>', self.select)
		self.canvas.tag_bind(self.tag, '<B1-Motion>', self.move)
		self.canvas.tag_bind(self.tag, '<ButtonRelease-1>', self.drop)

	def select(self, event):
		print 'hura'
		self.startx = event.x
		self.starty = event.y
		self.color = self.canvas.itemcget(self.tag, 'fill')
		
		self.canvas.itemconfig(self.tag, fill='orange')
		
	def move(self, event):
		print self.canvas.coords(self.tag)
		diffx = event.x - self.startx
		diffy = event.y - self.starty 
		self.canvas.move(self.tag, diffx, diffy)
		self.startx = event.x
		self.starty = event.y
		
	def drop(self, event):
		self.canvas.itemconfig(self.tag, fill=self.color)
	
class App(object):
	
	def __init__(self, master):
		#canvas
		self.color = 'blue'
		self.canvas = Canvas(master, width=500, height=500, bg='white')
		self.canvas.pack()
		self.item = self.canvas.create_rectangle(1,1,1,1)
		
		#toolbar
		image = Image.open("smiley.jpg")
		photo = ImageTk.PhotoImage(image)
		toolbar = Frame(master)
		self.button1 = Button(toolbar, image=photo, command=self.draw_rectangle)
		self.button1.image = photo
		self.button1.pack(side=LEFT, padx=2, pady=2)
		self.button2 = Button(toolbar, text='oval', command=self.draw_oval)
		self.button2.pack(side=LEFT, padx=2, pady=2)
		self.button3 = Button(toolbar, text='line', command=self.draw_line)
		self.button3.pack(side=LEFT, padx=2, pady=2)
		self.entry = Entry(toolbar)
		self.entry.pack(side=LEFT, padx=2, pady=2)
		self.button4 = Button(toolbar, text='ok', command=self.choose_color)
		self.button4.pack(side=LEFT, padx=2, pady=2)
		self.button5 = Button(toolbar, text='save', command=self.save_file)
		self.button5.pack(side=LEFT, padx=2, pady=2)
		toolbar.pack(side=TOP)
		
		#statusbar
		self.status = StatusBar(master)
		self.status.pack(side=BOTTOM, fill=X)
		self.canvas.bind('<B1-Motion>', self.coords)
		
	def coords(self, event):
		string = event.x
		self.status.set('x=%d; y=%d; color=%s', event.x, event.y, self.color)
	def save_file(self):
		self.canvas.update()
		self.canvas.postscript(file="postscript.ps", colormode='color')
	
	def choose_color(self):
		self.color = self.entry.get()
	
	def draw_rectangle(self):
		self.option = 'rectangle'
		self.bindings()
		
	def draw_oval(self):
		self.option = 'oval'
		self.bindings()
		
	def draw_line(self):
		self.option = 'line'
		self.bindings()
		
	def bindings(self):
		self.canvas.bind('<Button-3>', self.starting_point)
		self.canvas.bind('<B3-Motion>', self.resize)
		self.canvas.bind('<ButtonRelease-3>', self.finishing_point)

	def starting_point(self, event):
		self.startx = event.x
		self.starty = event.y
	
	def resize(self, event):
		self.canvas.delete(self.item)
		self.endx = event.x
		self.endy = event.y
		if self.option == 'rectangle':
			self.item = self.canvas.create_rectangle(self.startx, self.starty, self.endx, self.endy, fill=self.color)
		elif self.option == 'oval':
			self.item = self.canvas.create_oval(self.startx, self.starty, self.endx, self.endy, fill=self.color)
		elif self.option == 'line':
			self.item = self.canvas.create_line(self.startx, self.starty, self.endx, self.endy, fill=self.color)
	def finishing_point(self, event):
		self.item = Draggable(self.canvas, self.item)
		self.canvas.unbind('<Button-3>')
		self.canvas.unbind('<B3-Motion>')
		self.canvas.unbind('<ButtonRelease-3>')
		
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
		
def dist_between_points(x1,y1,x2,y2):
	return ((x1-x2)**2 + (y1-y2)**2)**(0.5)

root = Tk()
app = App(root)
root.mainloop()
