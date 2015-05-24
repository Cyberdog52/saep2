def f(x):
	if x > 0:
		return 0
	else:
		return 1


def g(x):
	if x > 0:
		return 1
	else:
		return 0

def main(x):
	return g(f(x))

def expected_result():
    return [0,1]



