#Written by Chris Keeler on July 1st, 2015

from fsm import *
from testing import *

def runTests(yourFSM,answerKeyFileName,testStringsFileName):
	tests = getLines(testStringsFileName)
	answerKey = getLines(answerKeyFileName)
	testAnswers = []

	for test in tests:
		if yourFSM.parseString(test):
			testAnswers.append('T')
		else:
			testAnswers.append('F')

	score = checkAnswers(answerKey,testAnswers)
	print "Score is: "+str(len(answerKey)-score)+"/"+str(len(answerKey))


def oddNumZeroesAndOnes():
	oddFSM = FSM()
	stateOne = State('1')
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

	runTests(oddFSM,"tests/FSMs/oddOnesAndZeroesAnswers.txt","tests/FSMs/binaryTests.txt")

def nZeroesNOnes():
	evenPDA = PDA()
	
	stateOne = State('1',True)
	stateTwo = State('2',True)

	evenPDA.addState(stateOne)
	evenPDA.addState(stateTwo)

	stateOne.addTransition(PDA_Transition(stateOne,'0','X','#'))
	stateOne.addTransition(PDA_Transition(stateTwo,'1','#','X'))
	stateTwo.addTransition(PDA_Transition(stateTwo,'1','#','X'))

	runTests(evenPDA,"tests/FSMs/nZeroesNOnesAnswers.txt","tests/FSMs/binaryTests.txt")
	
#oddNumZeroesAndOnes()
nZeroesNOnes()