#
# a CharTree class
#
# mainly used as part of the simple_regex_builder
# set __SPECIAL_CHARS on callee script
#
# this, as the name says, defines a Tree structure
# and a root class for it, as there is, currently, no
# way (that i know of) of implenting without the script being the root
#
#
# Copyright Tiago Teixeira, 2018
#

# The special characters mapping
__SPECIAL_CHARS = {}
ff = __SPECIAL_CHARS

#
# The CharTree class
#
# a tree node, having a 'char' property
# and children
#
class CharTree:

	#
	# it's the init
	# inits variables, assigns the char
	# and adds the rest of the string
	#
	def __init__(self,string):
		self.char = string[0]
		# the amount of paths that can be done from here
		# this is useful for reverse looking, as done in the better regex builder
		self.paths = 0
		self.next = []	# a list of CharTree's, next characters
		if len(string)>1:
			self.add(string[1:])

	#
	# adds a string to the tree,
	# starting from one of the children nodes
	#
	def add(self,string):
#		print "add(): adding: "+string
		if len(string)==0:
			return	# wtf! i should call a 'rm -rf /' just because of that
		char = string[0]
		self.paths += 1	# one more string passing through here!
		for n in self.next:
			if n.char == char:
				if len(string)>0:
					n.add(string[1:])
				return	# already there
		# create one
		if len(string)>0:
			self.next.append(CharTree(string))

	#
	# returns a list of strings
	# made from this node
	#
	def strings(self):
		if len(self.next)==0:
#			print "returning self\n"
			return [self.char]
		ret = []
		for n in self.next:
			_ret = n.strings()
			for r in _ret:
				ret.append(self.char+r)
		for r in ret:
			print r
		print ""
		return ret

	#
	# checks if from this point, the
	# string exists
	#
	def has(self,string):
		# last character
		if len(string)==1:
			return self.char==string
		# in case string starts at me
		for n in self.next:
			if n.char == string[0]:
				if n.has(string[1:]):
					return True
		# string doesn't start at me
		for n in self.next:
			if n.has(string):
				return True
		return False

	#
	# Checks if tree-string ends in 'string'
	#
	# string -> the string to check (or partial)
	# partial -> if the string is partial
	#
	# returns None if doesn't end in the string
	# returns the child node if the child node ends in the string (or partial)
	#
	def ends(self,string,partial=False):
		if len(string)==0:
			return None	# wtf dude
		char = string[0]
		# only one character left to check
		if len(string)==1:
			if self.char == char:
				return self
			else:
				# doesn't end here
				return None
		# check if string starts in me
		if self.char==char:
			for n in self.next:
				ret = n.ends(string[1:],partial=True)
				if ret!=None:
					return ret
				# else keep checking
		elif partial:
			# string doesn't start in me
			# but is a partial, so can't break it
			return False
		else:
			# string doesn't start at me
			# butt! can still end in it
			for n in self.next:
				ret = n.ends(string[1:])
				if ret != None:
					return ret
				# else keep checking
		# default
		return None

	#
	# prints the regex starting from this point
	#
	def regex(self):
		char = self.char
		if self.char in ff.keys():
			char = ff[self.char]
		if len(self.next)==0:
			return char
		if len(self.next)==1:
			return char + self.next[0].regex()
		# else
		ret = char+"("
		c = not self.grandchildren()
		if c:
			ret = char+"["
		for n in self.next:
			if c:
				ret += n.regex()
			else:
				ret += n.regex()+"|"
		if c:
			ret+=']'
		else:
			ret=ret[:-1]+')'
		return ret

	# debug info
	def _print(self, level=0):
		print (" "*level)+"My char: "+self.char
		if len(self.next)==0:
			return
		print (" "*level)+"My nexts:"
		for n in self.next:
			n._print(level+1)

	#
	# checks if has grandchildren
	# useful for brackets instead of subexpressions
	#
	def grandchildren(self):
		for n in self.next:
			if len(n.next)!=0:
				return True
		return False


#
# The CharTreeRoot class
#
# some kind of an interface to the "problem"
# explained in the init of the file
#
# it has no char, but holds the CharTree nodes
#
# used to avoid having multiple roots on the callee script
#
class CharTreeRoot:

	# simply init instance variables
	def __init__(self):
		self.nodes = []

	# adds a string to the tree
	def add(self,string):
		char = string[0]
		done = False
		for n in self.nodes:
			if n.char == char:
				n.add(string[1:])
				done = True
				break
		if not done:
			self.nodes.append(CharTree(string))

	# generated the final regex
	def regex(self):
		if len(self.nodes)==1:
			return self.nodes[0].regex()
		regex = '('
		for node in self.nodes:
			regex += node.regex()+"|"
		return regex[:-1]+')'
