#!/usr/bin/python

# Filename: Python.py
# Author:   Aaron Karper
# Description:
#           Capturing some OpenCV calls in classes for better organisation.
import cv

from shapes import *
from helpers import Struct



class Image(
		Struct("channels", "depth", "height", "nChannels", "origin",
			"tostring", "width")):
	def __init__(self, frame):
		self.raw = frame
	@staticmethod
	def fromFile(filename):
		return Image(cv.LoadImage(filename))
	def meFromFile(self,filename):
		self.raw = cv.LoadImage(filename)
	def draw(self,shape):
		shape.drawOn(self)
	@property
	def dim(self):
		return self.raw.width,self.raw.height
	def toBw(self):
		new = cv.CreateImage(self.dim,cv.IPL_DEPTH_8U,1)
		cv.CvtColor(self.raw,new,cv.CV_BGR2GRAY)
		return Image(new)
	def subrect(self,rect,*args):
		try:
			x1,y1,x2,y2 = rect
		except:
			try:
				(x1,y1),(x2,y2) = rect
			except:
				x1 = rect
				y1,x2,y2 = args[:3]
		return Image(cv.GetSubRect(self.raw,(x1,y1,x2-x1,y2-y1)))
	def toFile(self,filename):
		return cv.SaveImage(filename,self.raw)
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

	@property
	def framerate(self):
		return cv.GetCaptureProperty(self.capture,
				cv.CV_CAP_PROP_FPS)

