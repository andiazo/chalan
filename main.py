from src.parser import parse_string

def parse_file(filename: str, display: bool):
	with open(filename, 'r') as f:
		for line in f:
			parse_string(line, display)

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:

		display = True

		try:
			if len(argv) >= 3:
				if argv[2] == 'true':
					display = True
				elif argv[2] == 'false':
					display = False
				else:
					raise ValueError(f'{argv[2]} should be either true or false')
		except Exception as e:
			print('Exception:', e)
		else:
			parse_file('chalanexamples/examples/' + argv[1], display)
	
