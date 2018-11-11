#!/usr/bin/python2
#
# Regex Builder
#
# from a list of words
# simple regex's (i hope)
#
# currently only accepting alphanumeric and some special (escapable) characters
# which can be defined at __SPECIAL_CHARS as a mapping (dictionary, with key being
# the special character and the value being the escaped, printable, character)
#
#
# Copyright Tiago Teixeira, 2018
#
from sys import argv
import CharTree as ct

__SPECIAL_CHARS = {
	'-':'\\-',
	'/':'\\/',
	'\\':'\\\\'
	# add more here
}

#
# prints usage, when used as executable file
#
def __help(argv_0=argv[0]):
	print "usage: %s < <word1> [<word2>...] | -f <words.txt> >" % argv_0
	print "\twhere words.txt is a list of words,\n\tone word per line"
	return 1

#
# reads words from file
#
def from_file(filename):
	# read file lines
	try:
		f = open(filename,"r")
		lines = f.readlines()
	except IOError:
		print "failed to read from file"
		return []
	f.close()
	return lines

def __main(params):
	lines = []
	if '-f' in params and len(params)==2:	# -f filename
		for p in params:
			if p != '-f':
				lines = from_file(p)
		if lines == []:
			return __help()
	else:
		lines = params

	print get_regex(lines)


def get_regex(lines=[]):
	ct.__SPECIAL_CHARS = __SPECIAL_CHARS
	if len(lines)==0:
		print "no words in input"
		return 1

	for i in range(len(lines)):
		lines[i] = lines[i].lower()	# hackerman

	regex = ''

	# the 'roots' of CharTree's
	begs = []

	lines.sort()	# simplicity ?
	root = ct.CharTreeRoot()
	for line in lines:
		root.add(line)
	return root.regex()

if __name__=='__main__':
	if len(argv)<2:
		exit(__help(argv[0]))
	exit(__main(argv[1:]))
