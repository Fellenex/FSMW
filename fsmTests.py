#Written by Chris Keeler on
	#July 1st, 2015
	#November 5th/6th 2015

from fsm import *
from testing import *

def oddNumZeroesAndOnes():
	oddFSM = FSM()
	stateOne = State('1', True)
	stateTwo = State('2')
	stateThree = State('3')
	stateFour = State('4', True)
	oddFSM.addState(stateOne)
	oddFSM.addState(stateTwo)
	oddFSM.addState(stateThree)
	oddFSM.addState(stateFour)

	#odd number of 1s
	stateOne.addTransition(Transition(stateTwo,'1')) 	#odd number of 1s
	stateTwo.addTransition(Transition(stateOne,'1')) 	#even number of 1s
	
	stateOne.addTransition(Transition(stateThree,'0')) 	#odd number of 0s
	stateThree.addTransition(Transition(stateOne,'0'))	#even number of 0s

	stateTwo.addTransition(Transition(stateFour,'0'))	#odd number of 0s
	stateFour.addTransition(Transition(stateTwo,'0'))	#even number of 0s

	stateThree.addTransition(Transition(stateFour,'1'))	#odd number of 1s
	stateFour.addTransition(Transition(stateThree,'1'))	#even number of 1s

	return oddFSM

def nZeroesNOnes():
	evenPDA = PDA()
	
	stateOne = State('1',True)
	stateTwo = State('2',True)

	evenPDA.addState(stateOne)
	evenPDA.addState(stateTwo)

	stateOne.addTransition(PDA_Transition(stateOne,'0','X','#'))
	stateOne.addTransition(PDA_Transition(stateTwo,'1','#','X'))
	stateTwo.addTransition(PDA_Transition(stateTwo,'1','#','X'))

	return evenPDA

#An NFA with n+1 states which results in a DFA with 2^n states.
def canonicalWorstCase(_n):

	canonFSM = FSM()

	stateList = []

	for i in range(_n-1):
		stateList.append(State(str(i)))

	stateList.append(State(str(i+1),True))

	stateList[0].addTransition(Transition(stateList[1], 'a'))
	stateList[0].addTransition(Transition(stateList[1], 'a'))
	stateList[0].addTransition(Transition(stateList[1], 'b'))

	for i in range(1,len(stateList)-1):
		stateList[i].addTransition(Transition(stateList[i+1], 'a'))
		stateList[i].addTransition(Transition(stateList[i+1], 'b'))

	for s in stateList:
		canonFSM.addState(s)

	return canonFSM

def testOne():
	one = State('1')
	two = State('2')
	three = State('3')
	four = State('4', True)
	five = State('5')

	one.addTransition(Transition(two,'a'))
	one.addTransition(Transition(three,'a'))

	two.addTransition(Transition(three,'b'))

	three.addTransition(Transition(two,'b'))
	three.addTransition(Transition(four,'b'))

	four.addTransition(Transition(five,'c'))

	five.addTransition(Transition(four,'c'))
	five.addTransition(Transition(five,'b'))

	testNFA = FSM(['a','b','c'],one)

	testNFA.addState(two)
	testNFA.addState(three)
	testNFA.addState(four)
	testNFA.addState(five)

	return testNFA

def assignmentQuestion():
	one = State('1',True)
	two = State('2')
	three = State('3')
	four = State('4')
	five = State('5')

	one.addTransition(Transition(two,'a'))
	one.addTransition(Transition(four,'a'))

	two.addTransition(Transition(two,'b'))
	two.addTransition(Transition(three,'b'))
	two.addTransition(Transition(four,'b'))

	three.addTransition(Transition(five,'c'))

	four.addTransition(Transition(two,'c'))
	four.addTransition(Transition(five,'b'))

	five.addTransition(Transition(one,'b'))
	five.addTransition(Transition(two,'b'))

	testNFA = FSM(['a','b','c'],one)

	testNFA.addState(two)
	testNFA.addState(three)
	testNFA.addState(four)
	testNFA.addState(five)

	return testNFA

def main():
	fsmOne = oddNumZeroesAndOnes()
	fsmTwo = nZeroesNOnes()
	runTests(fsmOne, "tests/FSMs/oddOnesAndZeroesAnswers.txt","tests/FSMs/binaryTests.txt")
	runTests(fsmTwo,"tests/FSMs/nZeroesNOnesAnswers.txt","tests/FSMs/binaryTests.txt")
