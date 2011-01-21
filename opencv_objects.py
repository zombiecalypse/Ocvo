#!/usr/bin/python

# Filename: Python.py
# Author:   Aaron Karper
# Description:
#           Capturing some OpenCV calls in classes for better organisation.
import cv

def allint(lst):
	if isinstance(lst,(list,tuple,set)):
		return map(allint, lst)
	else:
		return int(lst)
def alltuple(lst):
	if isinstance(lst,(list,set)):
		return tuple(map(alltuple,lst))
	else:
		return lst

class Shape(object):
	def __init__(self,color = cv.CV_RGB(1.,1.,1.),**args):
		self.color = color
		self.args = args
	# overwrite for the win
	def draw(self, img):
		pass
	# overwrite for greater win (for annotations, etc)
	def boundingBox(self):
		return ((0,0),(0,0))
class PolyLine(Shape):
	def __init__(self, close = False, *points, **args):
		Shape.__init__(self,**args)
		self.points = allint(points)
		self.close = close
	def draw(self,img):
		pts = alltuple(self.points)
		cv.PolyLine(img.raw,(pts,),int(self.close),
				self.color, **self.args) 
	def boundingBox(self):
		return ((min(p[0] for p in self.points),
			min(p[1] for p in self.points)),
			(max(p[0] for p in self.points),
			max(p[1] for p in self.points)))

class Circle(Shape):
	def __init__(self,color = cv.RGB(0,0,0), center=(0,0), radius=0, **args):
		Shape.__init__( color , **args)
		self.center = map(int,center)
		self.radius = int(radius)
	def draw(self,img):
		cv.Circle(img.raw, self.center, self.radius, self.color,
				**self.args)
	def boundingBox(self):
		cx,cy = self.center
		r     = self.radius
		return ((cx-r,cy-r),(cx+r,cy+r))
class Text(Shape):
	def __init__(self,text = "", origin = (0,0), font =
			cv.FONT_HERSHEY_SIMPLEX,**args):
		Shape.__init__(self, **args)
		self.text = text
		self.origin = map(int,origin)
		self.font = cv.InitFont(font,1.,1.)
	def boundingBox(self):
		size = cv.GetTextSize(self.text, self.font)
		return ( ( self.origin[0], self.origin[1]),
			( self.origin[0]+size[0], self.origin[1]+size[1]))
	def draw(self,img):
		cv.PutText(img.raw,self.text,tuple(allint(self.origin)), self.font, self.color)

class Image(object):
	def __init__(self, frame):
		self.raw = frame
	def draw(self,shape):
		shape.draw(self)
class Capture(object):
	@staticmethod
	def fromUrl(url):
		return Capture(url,cv.CaptureFromFile(url))
	def meFromUrl(self,url):
		self.name = url
		self.capture = cv.CaptureFromFile(url)
	def __init__(self,name,capture, buffersize = 10):
		self.name = name
		self.capture = capture
		self.framebuffer = [None,] * buffersize 
		self.writer_position = self.reader_position = 0
	@property
	def buffersize(self):
		return len(self.framebuffer)
	@property
	def frame(self):
		return self.framebuffer[self.reader_position]
	def _reader_pos_get(self):
		return self.reader_position
	def _reader_pos_set(self,val):
		new = val % self.buffersize
		if self.framebuffer[new] != None:
			self.reader_position = new
	reader_pos = property(_reader_pos_get,_reader_pos_set)
	def _writer_pos_get(self):
		return self.writer_position
	def _writer_pos_set(self,val):
		new = val % self.buffersize
		self.writer_position = new
	writer_pos = property(_writer_pos_get,_writer_pos_set)

	def nextFrame(self):
		frame = cv.QueryFrame(self.capture)
		if frame:
			self.framebuffer[self.writer_pos] = \
					Image(cv.CloneImage(frame))
			self.writer_pos += 1
			self.reader_pos += 1
		return self.frame
	def saveFrame(self):
		framenr = cv.GetCaptureProperty(self.capture,
				cv.CV_CAP_PROP_POS_FRAMES)
		cv.SaveImage("pics/%05i.png" % framenr, 
				self.framebuffer[self.reader_position].raw)
	def _get_frame_pos(self):
		return cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_POS_FRAMES)
	def _set_frame_pos(self,val):
		return cv.SetCaptureProperty(self.capture,
				cv.CV_CAP_PROP_POS_FRAMES,val)
	framepos = property(_get_frame_pos,_set_frame_pos)
	def showFrame(self):
		cv.NamedWindow(self.name, cv.CV_WINDOW_AUTOSIZE)
		if self.frame:
			cv.ShowImage(self.name,self.frame.raw)
	def minus(self):
		self.reader_pos -= 1
	def plus(self):
		self.reader_pos += 1

	@property
	def framerate(self):
		return cv.GetCaptureProperty(self.capture,
				cv.CV_CAP_PROP_FPS)

