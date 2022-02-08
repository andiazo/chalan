import ply.lex as lex

# List of token names. This is always required
tokens = [
	'NUM',
	'VAR',
	'ID',
	'OPENB',
	'CLOSEB',
	'OPENP',
	'CLOSEP',
	'SEP',
	'LARROW',
	'RESERVED',
]


# Regular expression rules for simple tokens
t_ignore_COMMENT = r'(//.*)'

t_OPENB  = r'\['
t_CLOSEB  = r'\]'
t_OPENP  = r'\('
t_CLOSEP  = r'\)'

t_SEP = r'\,'

t_LARROW = r'\<\-'

def t_ID(t: lex.LexToken):
	r'[a-zA-Z](\w|\d)*'
	import re
	if t.value == 'var':
		t.type = 'VAR'
	elif re.match(r'(rachas|dotop|size|range|avg)', t.value):
		t.type = 'RESERVED'
	elif re.match(r'\<\-', t.value):
		t.type = 'LARROW'
	return t


# A regular expression rule with some action code
def t_NUM(t: lex.LexToken):
	r'-?\d+(\.\d+)?([eE][+-]?\d+)?'
	if float(t.value) != int(float(t.value)):
		t.value = float(t.value)
	else:
		t.value = int(float(t.value))
	return t

# Comment state
states = (
  ('ccomment','exclusive'),
)

def t_COMMENT(t):
	r'/\*(.|\r|\n)*'
	t.lexer.begin('ccomment')

def t_ccomment_COMMENT(t):
	r'(.|\r|\n)*\*/'
	# End of comment
	t.lexer.begin('INITIAL')

# Ignored characters (whitespace)
t_ccomment_ignore = " \t\n"

# For bad characters, we just skip over it
def t_ccomment_error(t):
	t.lexer.skip(1)

# Define a rule so we can track line numbers
def t_newline(t: lex.LexToken):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t: lex.LexToken):
	print("Illegal character", t.value)
	t.lexer.skip(1)

# EOF handling rule
# def t_eof(t: lex.LexToken):
# 	# Get more input (Example)
# 	more = input('... ')
# 	if more:
# 		t.lexer.input(more)
# 		return t.lexer.token()
# 	return None

# Build the lexer
lexer = lex.lex()


if __name__ == '__main__':
	# Give the lexer some input
	lexer.input(input("> "))

	# Tokenize
	while True:
		tok = lexer.token()
		if not tok:
			break      # No more input
		print(tok)