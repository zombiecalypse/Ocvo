#!/usr/bin/python

# Filename: helpers.py
# Author:   Aaron Karper
# Created:  2011-01-21
# Description:
#           helper methods

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

def Struct(*attrs,**opts):
	dict = {}
	if opts.has_key("key"):
		key = opts["key"]
	else:
		key = "raw"
	for i in attrs:
		dict[i]= property(lambda slf: getattr(getattr(slf,key),i),doc="%s.%s" % (key,i))
	return type('Struct',(object,),dict)

#class Struct(type):
	#def __new__(self,name,bases,dict):
		#if dict.has_key('__raw__'):
			#raw = dict['__raw__']
		#else:
			#raw = "_raw"
		#for i in dict['__readonly__']:
			#dict[i]= property(lambda slf: getattr(getattr(slf,raw),i))
		#return type(name, bases, dict)
