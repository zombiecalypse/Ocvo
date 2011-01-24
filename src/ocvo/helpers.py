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

def Struct(*attrs):
	dict = {}
	for i in attrs:
		dict[i]= property(lambda slf: getattr(slf._raw,i))
	return type('Struct',tuple(),dict)

#class Struct(type):
	#def __new__(self,name,bases,dict):
		#if dict.has_key('__raw__'):
			#raw = dict['__raw__']
		#else:
			#raw = "_raw"
		#for i in dict['__readonly__']:
			#dict[i]= property(lambda slf: getattr(getattr(slf,raw),i))
		#return type(name, bases, dict)
