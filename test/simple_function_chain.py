def chain4(asdf):
	return asdf

def chain3(x):
	return chain4(x)

def chain2(y):
	return chain3(y)

def chain1(asdf):
	return chain2(asdf)

def main (x):
	return chain1(x)
