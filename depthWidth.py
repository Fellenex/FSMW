#Written by Chris Keeler on
	#November 5th/6th 2015

from fsmTests import *
from constants import *
from NFAtoDFA import *

import difflib

class SUT():
	def __init__(self, _label, _string='', _path=[]):
		self.label = _label
		self.string = _string
		self.path = _path

	
	#Print output for an SUT
	def toString(self):
		print self
		print "\tL:"+self.label
		print "\tS:"+self.string
		pathString = "["+self.path[0]

		for i in range(1, len(self.path)):
			#print "Adding path["+str(i)+"]"
			pathString += ", "+self.path[i]

		pathString += "]"
		print "\tV:"+str(pathString)
		print UNDERLINE_BREAK

	def __eq__(self, _sutTwo):
		identical = True

		if not(self.label == _sutTwo.label):
			identical = False

		elif not(self.string == _sutTwo.string):
			identical = False

		elif not(self.path == _sutTwo.path):
			identical = False

		return identical

	def __neq__(self, _sutTwo):
		return not(self==_sutTwo)

	#Returns the next character which should be used in a transition given how much this SUT has already captured from _s
	#self.string should be a prefix of _s
	def nextChar(self, _s):
		c = ''
		for i,j in enumerate(difflib.ndiff(self.string, _s)):
			if j[0] == ' ':
				continue
			elif j[0] == '-':
				print(u'Delete "{}" from position {}'.format(j[-1],i))
			elif j[0] == '+':
				print(u'Add "{}" to position {}'.format(j[-1],i))
				if c=='':
					c = j[-1]
		print
		return c



#Uses this SUT to generate a new one with the same information, and more from the supplied transition object.
def extendSUT(_sut, _transition):
	newLabel = _transition.destination.label
	newString = _sut.string + _transition.label
	newPath = list(_sut.path)
	newPath.append(newLabel)
		
	return SUT(newLabel, newString, newPath)


#Create an initial SUT for some _nfa
def initialSUT(_nfa):
	return SUT(_nfa.startState.label, '', [_nfa.startState.label])


#Parameters:
#	_nfa: An _nfa to be measured
#
#Return Value:
#	sutList: A list of SUTs with depth _l, from _nfa
#
#Creates a list of SUTs for an NFA with all strings of length _l
#
def depthSUTs(_l, _nfa):
	sutList = []
	
	#Always pop/push stateQueue and partialComputations together
	stateQueue = [] #A list of states yet to be explored
	partialComputations = [] #A list of SUTs yet to reach depth _l

	#Seed the state queue with the starting state
	stateQueue.append(_nfa.startState)

	#Seed the partial computations with the length 0 computation
	partialComputations.append(initialSUT(_nfa))

	while len(stateQueue) > 0:
		activeState = stateQueue.pop()
		activeSUT = partialComputations.pop()

		debug("Active State: "+activeState.label)

		#l+1 because we count initial state as the first element in the path, where 0 transitions have been taken.
		if len(activeSUT.path) == _l+1:
			#We cannot go further from this SUT, since we've already reached maximal depth
			debug("Finished with this SUT")
			continue

		elif len(activeSUT.path) > _l+1:
			print "Error, should not have gotten here"
			exit(99)

		else:
			#loop through every transition of the current state
			for tr in activeState.transitions:
				debug("Active Transition:")
				tr.toString()
				
				extendedSUT = extendSUT(activeSUT,tr)

				#E-SUT not in P ==> E-SUT not in C
				if not(extendedSUT in partialComputations):
					debug("Adding E-SUT to P and S")
					partialComputations.append(extendedSUT)
					stateQueue.append(tr.destination)

					if len(extendedSUT.path)-1 == _l:
						#We add it to the list of SUTs which we will return as having depth l
						sutList.append(extendedSUT)
						debug("Adding E-SUT to C")

	return sutList


#Parameters:
#	_nfa: An _nfa to be measured
#
#Return Value:
#	sutList: A list of SUTs with string _s
#
#Creates a list of SUTs for an NFA with some supplied string, _s
#
def stringSUTs(_s, _nfa):
	sutList = []
	
	#Always pop/push stateQueue and partialComputations together
	stateQueue = [] #A list of states yet to be explored
	partialComputations = [] #A list of SUTs yet to reach depth _l

	#Seed the state queue with the starting state
	stateQueue.append(_nfa.startState)

	#Seed the partial computations with the length 0 computation
	partialComputations.append(initialSUT(_nfa))

	while len(stateQueue) > 0:
		activeState = stateQueue.pop()
		activeSUT = partialComputations.pop()

		debug("Active State: "+activeState.label)

		if not(_s.startswith(activeSUT.string)):
			print "Error, should not have gotten here"
			exit(98)

		else:
			trC = activeSUT.nextChar(_s)

		#loop through every transition of the current state
		for tr in activeState.getCharTransitions(trC):
			debug("Active Transition:")
			tr.toString()
			
			extendedSUT = extendSUT(activeSUT,tr)

			#E-SUT not in P ==> E-SUT not in C
			if not(extendedSUT in partialComputations):
				debug("Adding E-SUT to P and S")
				partialComputations.append(extendedSUT)
				stateQueue.append(tr.destination)

				if extendedSUT.string == _s:
					#We add it to the list of SUTs which we will return as having string s
					sutList.append(extendedSUT)
					debug("Adding E-SUT to C")

	return sutList


#Looks through a list of SUTs to find the path width
def sutPathWidth(_sutList):
	n = len(_sutList)

	definedPaths = []

	for sut in _sutList:
		pass

	return n


def depth(_fsm):
	pwDict = dict()
	for i in range(1,4):
		SUTs = depthSUTs(i, _fsm)
		pwDict[i] = len(SUTs)


	print "doneszo"

	print pwDict
	return pwDict


def sutEqualityTest():

	SUTone = SUT('1', '', [myFSM.startState])
	SUTtwo = SUT('1', '1', [myFSM.startState])
	SUTthree = SUT('1', '', [myFSM.startState])


	print SUTone
	print SUTtwo
	print SUTthree
	print SUTone == SUTthree
	print SUTone == SUTtwo
	print SUTtwo == SUTthree

	mL = [SUTone, SUTtwo]

	print SUTthree in mL


def strings():
	myFSM = oddNumZeroesAndOnes()

	testStrings = ['0','1','00','01','10','11','000','001','010','011','100','101','110','111']
	pwDict = dict()

	for s in testStrings:
		SUTs = stringSUTs(s, myFSM)
		pwDict[s] = len(SUTs)

	print "wumbo"

	print pwDict

def main():
	print "hello world"
	myFSM = oddNumZeroesAndOnes()
	depth(myFSM)

print "oops"
main()
print "now"