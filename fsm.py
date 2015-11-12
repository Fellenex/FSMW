#Written by Chris Keeler on June 23rd, 2015

import sys
from constants import *

#self.states is a list used to store all of an FSM's states.
class FSM():
	def __init__(self,_alphabet=[],_startState=None):
		self.deterministic = True
		self.states = []
		self.startState = _startState
		if not(_startState is None):
			self.states.append(_startState)
		self.alphabet = _alphabet

	def addState(self,_state):
		self.states.append(_state)

		#Assumes that the first state added is the starting state.
		if (self.startState == None) and (len(self.states) == 1):
			self.startState = _state

	def removeState(self,_state):
		if _state in self.states:
			self.states.remove(_state)
		else:
			"That state isn't even in here, ya goon."

	#Returns the state in _stateList which has _label as its label.
	def findState(self, _label):
		relevantStates = filter(lambda x : x.label == _label, self.states)

		if len(relevantStates) > 1:
			print "Error: Multiple states with duplicate label: "+_label
		
		elif len(relevantStates) == 0:
			print "Error: No state with label "+_label

		print "Was looking for a state with "+_label+" and found "+str(relevantStates[0].label)

		return relevantStates[0]

	#Sets the T/F value for this FSM's determinism.
	def determineDeterminism(self):
		self.deterministic = True
		for state in self.states:
			if not state.deterministic:
				self.deterministic = False

	def toString(self):
		for s in self.states:
			print s.label
			transitionString = "["
			for t in s.transitions:
				transitionString+=t.label+":"+t.destination.label+", "

			transitionString = transitionString[:-1]+"]"
			print transitionString
			print

	def parseString(self,_string):
		c=0
		activeState = self.startState
		stringSuccess = True

		#loop until we only have the empty string left
		while c<len(_string):
			stateStack=[]

			#look through all of the transitions of a state
			for t in activeState.transitions:

				#Special transition label to allow any alphabetic character
				if t.label == ALPHABETIC and _string[c].isalpha():
					stateStack.append(t.destination)

				#Special transition label to allow any numeric character
				elif t.label == NUMERIC and _string[c].isnumeric():
					stateStack.append(t.destination)

				#regular character match without character templates
				elif t.label == _string[c]:
					stateStack.append(t.destination)

				#matching the empty string
				elif t.label == EMPTY and c==(len(_string)-1):
					stateStack.append(t.destination)

				else:
					pass
					#maybe we can still find a match with another transition from this state


				#TODO handle non-determinism better than not at all
				#Lookback, options on the stack, etc

			if (len(stateStack) == 0):
				print "Couldn't find a transition to take from "+activeState.label
				badFormat(_string[c],c)
				stringSuccess = False

			elif (len(stateStack) == 1):
				print "Deterministic transition"
				print "Accepted "+_string[c]
				activeState = stateStack[0]
			
			else:
				print "Degree of nondeterminism: "+str(len(stateStack))

			c+=1

		#If we've successfully parsed every character, then we must check for a finishing state
		if activeState.accepting and stringSuccess:
			print _string+" is a valid string"
		else:
			print _string+" is an invalid string"

		return (activeState.accepting and stringSuccess)


#self.deterministic is a boolean used to represent the individual state's determinism
#self.transitions is a list used to store all of a State's outgoing transitions
#self.label is a string used to describe the state
#self.accepting is a boolean used to represent whether this is a final state
class State():
	def __init__(self,_label,_accepting=False):
		self.deterministic = True
		self.transitions = []
		self.label = _label
		self.accepting = _accepting

	def addTransition(self,_transition):
		#Determine if this makes this state non-deterministic
		for t in self.transitions:
			if _transition.label == t.label:
				self.deterministic = False

		self.transitions.append(_transition)

	def getTransitions(self):
		print map(lambda x: x.label, self.transitions)

	#Returns all transitions using the specified trigger character
	def getCharTransitions(self, _char):
		return filter(lambda x : x.label == _char, self.transitions)


#self.destination should be a State() object
#self.label should be a character
class Transition():
	def __init__(self,_destination,_label):
		self.destination = _destination
		self.label = _label


#PDAs are just like FSMs, but with a stack!
#This means they need to use PDA_Transition objects instead of regular Transition objects
class PDA(FSM):
	def __init__(self,_startState=None):
		self.deterministic = True
		self.stack = []
		self.states = []
		self.startState = _startState
	
	def parseString(self,_string):
		print "Attempting to parse "+_string
		c=0
		activeState = self.startState
		stringSuccess = True
		self.stack = [] #we reset the parse stack for every parse

		#loop until we only have the empty string left
		while c<len(_string):
			stateStack=[]
			transitionStack=[]

			#look through all of the transitions of a state
			for t in activeState.transitions:
				#Reject transitions which we cannot use based on the current state of the stack
				if t.pop != EMPTY:
					print "It wants me to pop "+t.pop
					print "\t"+str(transitionStack)
					if len(self.stack)==0:
						#Can't possibly pop from the stack!
						continue

					elif t.pop != self.stack[-1]:
						#Can't pop this symbol since it isn't on the top of the stack
						continue

				#Special transition label to allow any alphabetic character
				if t.label == ALPHABETIC and _string[c].isalpha():
					transitionStack.append(t)

				#Special transition label to allow any numeric character
				elif t.label == NUMERIC and _string[c].isnumeric():
					transitionStack.append(t)

				#regular character match without character templates
				elif t.label == _string[c]:
					transitionStack.append(t)

				#matching the empty string
				elif t.label == EMPTY and c==(len(_string)-1):
					transitionStack.append(t)

				else:
					pass
					#maybe we can still find a match with another transition from this state

				print "S: "+str(self.stack)

			print "D: "+str(self.stack)

			if (len(transitionStack) == 0):
				print "Couldn't find a transition to take from "+activeState.label
				badFormat(_string[c],c)
				stringSuccess = False

			elif (len(transitionStack) >= 1):
				if (len(transitionStack) > 1):
					print "Degree of nondeterminism: "+str(len(transitionStack))
				else:
					print "Deterministic transition using "+transitionStack[0].label
				
				print "\tA: "+str(self.stack)

				#TODO handle non-determinism
				activeTransition = transitionStack.pop()

				print "\tB: "+str(self.stack)

				#Pop first
				if activeTransition.pop != EMPTY:
					print "Getting ready to pop "+str(activeTransition.pop)
					print "\tC "+str(self.stack)

					if len(self.stack) == 0:
						print "Oh I couldn't possibly pop!"
						stringSuccess = False

					elif activeTransition.pop == self.stack[-1]:
						self.stack.pop()

					else:
						print "That is not a candidate for /r/popping"
						stringSuccess = False

				#Push second
				if activeTransition.push != EMPTY:
					self.stack.append(activeTransition.push)

				activeState = activeTransition.destination

			c+=1

		#If we've successfully parsed every character, then we must check for a finishing state
		if activeState.accepting and stringSuccess and len(self.stack)==0:
			print _string+" is a valid string"
		else:
			print _string+" is an invalid string"

		print "\tSize of stack is "+str(len(self.stack))
		print
		return (activeState.accepting and stringSuccess and len(self.stack)==0)


#self.destination should be a State() object
#self.label should be a character
#self.push should be a character
#self.pop should be a character
class PDA_Transition(Transition):
	def __init__(self,_destination,_label,_push,_pop):
		self.destination = _destination
		self.label = _label
		self.push = _push
		self.pop = _pop