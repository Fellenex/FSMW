#Used for the expression grammar non-terminal names, since
#they won't show up in assignment statements or Hoare assertions
EXPRESSION = '$'
EXPONENTS = '{'
MULTIDIV = '}'
ADDSUB = '%'
ATOMS = '&'

EMPTY = '#'
ALPHABETIC = '@'
NUMERIC = '#'
WHITESPACE = ' '

UNDERLINE_BREAK = "____________________________________________"

#Exits out of the parse when ill-formatted statements are found.
#Parameters:
#	spookyCharacter: A character which has been found to be in violation of the syntax
#	charIndex: The index at which the character was found
#Return Value:
#	None
#
def badFormat(spookyCharacter,charIndex):
	print "Unexpected Symbol: '"+spookyCharacter+"' found at index "+str(charIndex)
	#sys.exit(42)

DEBUG = True
def debug(_s):
	if DEBUG:
		print _s