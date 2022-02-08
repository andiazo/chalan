from distutils.log import error
from glob import glob
import ply.yacc as yacc
from .flex import tokens
from . import ast
var = {}

def p_expression(p):
	"""expression :
		| creation
		| insertion
		| access
	"""
	if len(p) > 1:
		p[0] = p[1]['exec']
		p[1]['exec'] = p[1]['blocks']


def p_expression_creation_treatments(p):
	"""creation : VAR ID OPENB tratamientos CLOSEB
	tratamientos : tratamientos SEP ID
			| ID"""
	global var
	if len(p) == 6:
		var[p[2]] = {'treatments': p[4],'blocks': [],'exec': []}
		p[0] = var[p[2]]
		p[0]['exec'] = p[0]['treatments']

	# treatments
	elif len(p) == 2:
			p[0] = [p[1]]
	elif len(p) == 4:
		# p[1] is treatments
		p[0] = p[1]
		p[0].append(p[3])

def p_expression_insertion(p):
	"""insertion : ID LARROW OPENB matrix CLOSEB
		| ID LARROW OPENB arr CLOSEB"""
	global var
	if p[1] in var:
		var[p[1]]['blocks'].append(p[4])
		p[0] = var[p[1]]

		# exec must be equal to blocks by default
		var[p[1]]['exec'] = p[0]['blocks']
	else:
		raise KeyError(f'{p[1]} does not exist')

def p_expression_matrix(p):
	"""matrix : matrix SEP OPENB arr CLOSEB
			| OPENB arr CLOSEB """

	if len(p) == 4:
		p[0] = [p[2]]
	else:
		p[0] = p[1]
		p[0].append(p[4])

def p_expression_arr(p):
	"""arr : arr SEP NUM
		| NUM
		arr_str : arr_str SEP ID
		| ID
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])

def p_expression_access(p):
	"""access : access OPENB arr_str CLOSEB
		| access OPENB arr CLOSEB
		| other
	"""
	global var


	# index recursion
	if len(p) == 5:
			# Important: p[1] is an instance of var
		if type(p[1]['exec']) is int or type(p[1]['exec']) is float:
			raise IndexError(f'Can\'t access to an index of function ')

		if (0 in p[3] or 'treatments' in p[3]) and len(p[3]) != 1:
			raise IndexError(f'Can\'t access to all elements with multiple indexes given')

		# Get all the elements
		elif (0 in p[3] or 'treatments' in p[3]):
			if p[3][0] == 0:
				p[1]['exec'] = p[1]['exec']
			elif p[3][0] == 'treatments':
				p[1]['exec'] = ast.transpose(p[1]['exec'])

		else:
			if not type(p[1]['exec'][0]) is list:
				p[1]['exec'] = [p[1]['exec']]
			results = []
			for index in p[3]:
				result = []
				for data in p[1]['exec']:
					# Access to blocks
					if type(index) is int:

						# if data or range(data) exists in
						#  and index retrieves the expected value
						if (data == p[1]['blocks'][index-1] and\
							 data in p[1]['blocks']) or \
						(data == ast.range_of(p[1]['blocks'][index-1]) and\
							 data in ast.range_of(p[1]['blocks'])):
							result.append(data)

						# if transpose(data) or transpose(range(data)) exists
						#  return the information located at data[index-1]
						elif (data in ast.transpose(p[1]['blocks'])) or \
							(data in ast.transpose(ast.range_of(p[1]['blocks']))):
							result.append(data[index-1])

					# Access to treatments
					elif type(index) is str:
						treatment_index = p[1]['treatments'].index(index)

						# if data or range(data) exists in
						#  and index retrieves the expected value
						if (data in p[1]['blocks']) or (data in ast.range_of(p[1]['blocks'])):
							result.append(data[treatment_index])

						# same logic different result ¯\_(ツ)_/¯
						elif (data == ast.transpose(p[1]['blocks'])[treatment_index] and\
							 data in ast.transpose(p[1]['blocks'])) or \
							(data == ast.transpose(ast.range_of(p[1]['blocks']))[treatment_index] and\
								 data in ast.transpose(ast.range_of(p[1]['blocks']))):
							result.append(data)
					else:
						raise TypeError('Index must be integer or string name')

				results.append(result[0] if len(result) == 1 else result)
			p[1]['exec'] = results if len(results) != 1 else results[0]
		p[0] = p[1]
	# other
	elif len(p) == 2:
		p[0] = p[1]


def p_expression_other(p):
	"""other : ID
		 | function
			"""
	if type(p[1]) is str:
		var[p[1]]['exec'] = var[p[1]]['blocks']
		p[0] = var[p[1]]
	else:
		p[0] = p[1]

def p_expression_function(p):
	"""function : RESERVED OPENP params CLOSEP"""
	global var
	if p[1] == 'dotop' or p[1] == 'rachas':
		p[3][0]['exec'] = ast.functions[p[1]](p[3])
		p[0] = p[3][0]

	elif p[1] in ast.functions.keys():
		p[3] = ast.functions[p[1]](p[3])
		p[0] = p[3]

	else:
		p[0] = p[3]

def p_params(p):
	"""params : params SEP NUM
		| params SEP access
		| params SEP ID
		| NUM
		| access
		| ID
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_error(p):
	if p:
		print("Syntax error at '%s'" % p.value, p)
	else:
		print("Syntax error at EOF")

parser = yacc.yacc(debug=True, start='expression')

def parse_string(s: str, display = True):
	try:
		result = parser.parse(s)
		if result is not None:
			if display:
				print("Codigo: ", s, '\nResultado: ', result, end='\n\n')
			else:
				print(result)
	except Exception as e:
		print(">", s, '\n****>', e, end='\n\n')

if __name__ == '__main__':
	while True:
		try:
			s = input()
		except EOFError:
			break
		if not s: continue
		parse_string(s)

