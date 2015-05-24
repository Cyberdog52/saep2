def g(x):
	if x > 1:
		return 1
	else:
		return 0

def main(x):
	y = g(x)
	return g(x) + y

def expected_result():
    return [0, 2]



