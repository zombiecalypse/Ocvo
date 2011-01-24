#!/usr/bin/python

# Filename: shapes.py
# Author:   Aaron Karper
# Created:  2011-01-21
# Description:
#           Shapes can draw themselves on an image.
#
import cv
import helpers as _h

class Shape(object):
	# overwrite for the win
	def drawOn(self, img):
		pass
	# overwrite for greater win (for annotations, etc)
	def boundingBox(self):
		return ((0,0),(0,0))

# Unicolor
class SimpleShape(object):
	defaultColor = cv.CV_RGB(255,255,255)
	def __init__(self,color = None,**args):
		self.color = color or self.defaultColor
		self.args = args
class Rectangle(SimpleShape):
	def __init__(self,p1,p2,color = None,**args):
		SimpleShape.__init__(self,color,**args)
		self.x1 = min(p1[0],p2[0])
		self.x2 = max(p1[0],p2[0])
		self.y1 = min(p1[0],p2[0])
		self.y2 = max(p1[0],p2[0])
	@property
	def bottomleft(self):
		return (self.x1,self.y1)
	@property
	def topright(self):
		return (self.x2,self.y2)
	def boundingBox(self):
		return self
	def drawOn(self,img):
		cv.Rectangle(img,self.bottomleft,self.topright,
				self.color,**self.args)
class PolyLine(SimpleShape):
	def __init__(self, close = False, *points, **args):
		Shape.__init__(self,**args)
		self.points = _h.allint(points)
		self.close = close
	def drawOn(self,img):
		pts = _h.alltuple(self.points)
		cv.PolyLine(img.raw,(pts,),int(self.close),
				self.color, **self.args) 
	def boundingBox(self):
		return ((min(p[0] for p in self.points),
			min(p[1] for p in self.points)),
			(max(p[0] for p in self.points),
			max(p[1] for p in self.points)))

class Circle(SimpleShape):
	def __init__(self,color = cv.RGB(0,0,0), center=(0,0), radius=0, **args):
		Shape.__init__( color , **args)
		self.center = map(int,center)
		self.radius = int(radius)
	def drawOn(self,img):
		cv.Circle(img.raw, self.center, self.radius, self.color,
				**self.args)
	def boundingBox(self):
		cx,cy = self.center
		r     = self.radius
		return ((cx-r,cy-r),(cx+r,cy+r))
class Text(SimpleShape):
	def __init__(self,text = "", origin = (0,0), font =
			cv.FONT_HERSHEY_SIMPLEX, scale = (1.,1.),
			**args):
		Shape.__init__(self, **args)
		self.text = text
		self.origin = map(int,origin)
		self.font = cv.InitFont(font,*scale)
	def boundingBox(self):
		size = cv.GetTextSize(self.text, self.font)
		return ( ( self.origin[0], self.origin[1]),
			( self.origin[0]+size[0], self.origin[1]+size[1]))
	def drawOn(self,img):
		cv.PutText(img.raw,self.text,tuple(_h.allint(self.origin)),
				self.font, self.color)

class Composed(Shape):
	def __init__(self, *sub):
		self._subobjects = sub
