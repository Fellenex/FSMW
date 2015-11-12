#Written by Chris Keeler on
	#September 5th, 2015
	#November 5th/6th 2015

from fsm import *
from constants import *
from fsmTests import *
from collections import OrderedDict

#Converts a list of states into a string to be used as the merged state label.
def mergeStateLabels(_stateList):
	sortedList = sorted(_stateList)

	formatted = "{"+sortedList[0].label
	for i in range(1, len(sortedList)):
		formatted += ","+sortedList[i].label
	formatted+="}"

	return formatted

#Creates a list from _sequence without duplicate elements.
def makeCollectionUnique(_sequence):
	return list(OrderedDict.fromkeys(_sequence))

#Parameters:
#	_state: A state to be copied in shallow
#
#Return Value:
#	A state with the same label and acceptance as _state
#
def cloneState(_state):
	return State(_state.label, _state.accepting)

#Parameters:
#	_nfa: An _nfa to be turned into a DFA
#
#Return Value:
#	equivalentDFA: A DFA such that L(_nfa) == L(equivalentDFA)
#
def convertNFA(_nfa):
	if _nfa.deterministic:
		print "No conversion required! Already a DFA."
		return _nfa

	equivalentDFA = FSM()

	#Always push/pop oldStateQueue and newStateQueue together
	oldStateQueue = [] #each element is a state or a set of states from _nfa, to be cloned or merged (respectively) for equivalentDFA
	newStateQueue = [] #each element is a cloned or merged state in equivalentDFA, with transitions yet to be added

	#Assume only one start state.
	memoizedStates = [_nfa.startState.label] #We store them as labels because rediscovered states can be composed of a set of states
	oldStateQueue.append([_nfa.startState])

	#Create the equivalent DFA's start state and add it to the new states queue
	newStartState = cloneState(_nfa.startState)
	newStateQueue.append(newStartState)
	equivalentDFA.addState(newStartState)

	while len(oldStateQueue) > 0:
		debug("Length is "+str(len(oldStateQueue)))
		#We may be looking at a set of states, or just one state. (still always stored as a list)
		activeStateSet = oldStateQueue.pop(0)

		#However, we always create one state to represent the old one(s)
		activeNewState = newStateQueue.pop(0)

		for c in _nfa.alphabet:

			if len(activeStateSet) > 1:
				#We are looking at a set of states this time.
				#This means that we have to look at all of the transitions from all states, per character, before combining their destinations into merged states.
				#This also means that activeNewState is a merged state in equivalentDFA, so we don't care which
					#states the transitions came from originally, since activeNewState is now the source state

				#Collect the transitions using c, from all states
				currentTransitions = []
				for s in activeStateSet:
					currentTransitions += s.getCharTransitions(c)

			elif len(activeStateSet) == 1:
				currentTransitions = activeStateSet[0].getCharTransitions(c)

			else:
				print "Error, no states in activeStateSet."

			#Since NFA-->DFA conversion is worst-case 2^n blow-up of statespace, we hope that the number of transitions is sparse.
			#We take advantage of hopeful sparseness by checking for the lack of a transition prior to the existence of one.
			if len(currentTransitions) == 0:
				#No transitions with this character
				pass

			elif len(currentTransitions) == 1:
				#Deterministic transition with this character from this state

				#Since there is only one transition, there is only one destination
				destinationState = currentTransitions[0].destination

				#If we have already added this state, then don't add it again!
				if destinationState.label in memoizedStates:

					#However, we still need to add a transition with this state as its destination
					clonedState = equivalentDFA.findState(destinationState.label)
					clonedTransition = Transition(clonedState, c)

				else:
					clonedState = cloneState(destinationState)
					clonedTransition = Transition(clonedState, c)
					equivalentDFA.addState(clonedState)

					newStateQueue.append(clonedState)

					oldStateQueue.append([destinationState])

					memoizedStates.append(destinationState.label)

				activeNewState.addTransition(clonedTransition)

			elif len(currentTransitions) > 1:
				#Nondeterministic transition with this character from this state

				#Create a list of states based off of all of the transitions with this character
				destinationStateList = map(lambda x : x.destination, currentTransitions)

				#Remove duplicates so that we don't bother recomputing their transitions
				mergedStateList = makeCollectionUnique(destinationStateList)

				#Create a label for the merged state we are creating
				mergedStateLabel = mergeStateLabels(mergedStateList)

				#If we have already added this state, then don't add it again!
				if mergedStateLabel in memoizedStates:

					#However, we still need to add a transition with this state as its destination
					mergedState = equivalentDFA.findState(mergedStateLabel)
					mergedTransition = Transition(mergedState, c)

				else:
					#If any of the states in the set is accepting, then the new state is accepting.
					mergedAcceptance = False
					for s in mergedStateList:
						if s.accepting:
							mergedAcceptance = True
							break

					#Create a new state to represent the merged state, and add it to our equivalent DFA
					mergedState = State(mergedStateLabel, mergedAcceptance)
					mergedTransition = Transition(mergedState, c)
					equivalentDFA.addState(mergedState)

					#We want to use this as a future source state in our equivalent DFA
					newStateQueue.append(mergedState)

					#We want to use these states from _nfa as future source state sets to create our equivalent DFA
					oldStateQueue.append(mergedStateList)

					memoizedStates.append(mergedStateLabel)

				#Our current equivalent state gets a transition to the merged state with c, combining any nondeterminism
				activeNewState.addTransition(mergedTransition)

			else:
				print "Error, negative or NaN number of transitions"

	print "Finished conversion!"
	return equivalentDFA

#Takes an _nfa and converts it, while also outputting to the console some information regarding the conversion
def convertAndPrint(_nfa):
	_nfa.determineDeterminism()
	_nfa.toString()

	if _nfa.deterministic:
		dfa = _nfa
	else:
		dfa = convertNFA(_nfa)

	print "###"
	dfa.toString()


testFSMs = [testOne(), assignmentQuestion(), canonicalWorstCase(4)]

for t in range(len(testFSMs)):
	print "Converting new FSM:"
	convertAndPrint(testFSMs[t])