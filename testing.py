#Written by Chris Keeler on July 1st, 2015

#Retrieves the contents of a file with linebreaks,
#	splitting each line into its own string
def getLines(fileName):
	with open(fileName) as f:
		lines = f.readlines()
	stripped = []
	for line in lines:
		stripped.append(line.rstrip('\n'))
	return stripped

#Compares two lists of values to compare the real acceptance vs. its intended acceptance
def checkAnswers(answerKey,testAnswers):
	offenses = 0

	if not(len(answerKey) == len(testAnswers)):
		print "Answer lists' lengths do not match"

	for i in range(len(answerKey)):
		if str(answerKey[i]) != str(testAnswers[i]):
			print "comparing: "+str(answerKey[i])+" with "+str(testAnswers[i])+" at index "+str(i)
			offenses+=1

	return offenses

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