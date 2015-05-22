def chain4(asdf):
	return asdf

def chain3(x, y, z):
	if x > 1:
		if y > 1:
			if z > 1:
				return chain4(42)
	return chain4(10000)

def chain2(y):
	return chain3(y, y, y)

def chain1(asdf, a):
	return chain2(asdf+a)

def main (x,y):
	return chain1(x,y)

def expected_result():
    return [42, 1000]
