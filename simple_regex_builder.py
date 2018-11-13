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
	lines = []
	try:
		f = open(filename,"r")
		_t = f.readlines()
		for line in _t:
			# chomp
			lines.append(line[:-1])
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

#
# the main function of the 'module'
#
def get_regex(lines=[]):
	ct.__SPECIAL_CHARS = __SPECIAL_CHARS
	if len(lines)==0:
		print "no words in input"
		return 1

	# remove duplicates
	lines = list(set(lines))

#	for i in range(len(lines)):
#		lines[i] = lines[i].lower()	# hackerman

	lines.sort()	# simplicity ?

	root = ct.CharTreeRoot()
	for line in lines:
		if len(line)>0:
			root.add(line)
	return root.regex()

# if its called not as module
if __name__=='__main__':
	if len(argv)<2:
		exit(__help(argv[0]))
	exit(__main(argv[1:]))
