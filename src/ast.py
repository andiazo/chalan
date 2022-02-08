from copy import deepcopy

def transpose(data):
	return list(map(list, zip(*data)))

def range_of(data: list):
	from operator import itemgetter
	results = []

	is_array = type(data[0]) is not list
	if is_array:
		data = [data]

	for matrix in data:
		a = [ i for (i,j) in sorted(enumerate(matrix), key=itemgetter(1))]

		result = [element for _, element in sorted(zip(a, range(1,len(a)+1)))]

		current = None
		i = j = None
		for r in range(1,len(a)+1):
			if current is None:
				current = matrix[result.index(r)]
				i = j = r
				continue

			if current == matrix[result.index(r)]:
				j += 1
			else:
				if j - i > 0:
					val = avg_of([n for n in range(i,j+1)])
					for n in range(i,j+1):
						result[result.index(n)] = val
				current = matrix[result.index(r)]
				i = j = r

		if j - i > 0:
			val = avg_of([n for n in range(i,j+1)])
			for n in range(i,j+1):
				result[result.index(n)] = val
		results.append(result)
	return results if not is_array else results[0]

def avg_of(matrix: list):
	if type(matrix[0]) is list:
		return avg_of([avg_of(m) for m in matrix])
	else:
		return sum(matrix)/len(matrix)

def size_of(matrix):
	if type(matrix[0]) is list:
		return sum([len(m) for m in matrix])
	else:
		return len(matrix)

def dotop(variable):
	"""
	Devuelve pareja (n, navg)
	n: resultado operacion punto
	n: promedio operacion punto
	"""
	model = variable[0]
	matrix = model['blocks']
	i = variable[1]
	j = variable[2]
	k = variable[3]
	n = 0
	navg = 0
	ndatos = len(sum(sum(matrix, []),[]))
	if i == j == k == 0:
		n = sum(sum(sum(matrix,[]),[]))
		navg = n/ndatos
	
	elif j == k == 0 and i > 0:
		n = sum(sum(matrix[i-1],[]))
		navg = n/ndatos

	elif i == k == 0 and j > 0:
		for l in range(len(matrix)):
			n += sum(matrix[l][j-1])
		navg = n/ndatos

	elif i > 0 and j > 0 and k > 0:
		return matrix[i-1][j-1][k-1], matrix[i-1][j-1][k-1]

	return n, navg 

def rachas(variable):
	# TODO: function rachas
	model = variable[0]
	matrix = model['blocks']
	tratamientos = model['treatments']
	i = variable[1]
	j = variable[2]
	k = variable[3]
	n = 0
	union(matrix, tratamientos)
	cadenas = []
	rachas = []
	matrixrachas = []
	for l in range(len(matrix)):
		bloque = matrix[l]
		unsortl = sum(matrix[l],[])
		unionl = sum(matrix[l],[])
		unionl.sort()
		cadena_multicotl = cadenamulticot(unionl)
		cadenas.append(cadena_multicotl)

		racha = [1 for l in range(len(cadena_multicotl))]
		if len(cadena_multicotl) != 0:
			prev = cadena_multicotl[0]
			racha[0] = 1
			for l in range(1, len(cadena_multicotl)):
				if cadena_multicotl[l] == prev:
					racha[l] = racha[l-1]
				else:
					racha[l] += racha[l-1]
				prev = cadena_multicotl[l]
		rachas.append(racha)

		d_aux = [unionl, racha]
		matrixrachas.append(bloque)


	print("cadenas", cadenas, "rachas", rachas)
	
def union(matrix, tratamientos):
	print("union")
	aux = 1
	unions = []
	un = []
	unsort = []
	idx = []

	t_unions = []
	t_un = []
	t_unsort = []
	t_idx = []

	tr_m = deepcopy(matrix)
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			for k in range(len(matrix[i][j])):
				# multicotomizar con los tratamientos
				tr_m[i][j][k] = (matrix[i][j][k], tratamientos[j], aux)
				un.append(matrix[i][j][k])
				unsort.append(matrix[i][j][k])
				idx.append(aux)
				aux += 1
		unsort.sort()
		unions.append([unsort, un,idx])
		unsort = []
		un = []
		idx = []

	trmlist = []
	for i in range(len(tr_m)):
		for j in range(len(tr_m[i])):
			sort = sorted(tr_m[i][j], key=lambda tup: tup[0])
			trmlist += sort

		print("\n")

	print(trmlist)


	


def cadenamulticot(vector):
	mc = []
	for i in range(len(vector)):
		if vector[i] > 2:
			mc.append(1)
		else:
			mc.append(0)
	return mc

functions = {
	'range': range_of,
	'size' : size_of,
	'avg' : avg_of,
	'dotop': dotop,
	'rachas': rachas,
}

