#!/usr/bin/env python

from distutils.core import setup

setup(
		name='Ocvo',
		version='0.1',
		description='Objects for OpenCV',
		author='Aaron Karper',
		author_email='akarper@students.unibe.ch',
		packages=['ocvo'],
		package_dir = {'': 'src'})
