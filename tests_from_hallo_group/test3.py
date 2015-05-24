def main (x,y):

	s=func(func(x))+func(func2(func(x),func(y),func(x)))
	return 3

def func(x):
	if (x==4):
		return 5
	else:
		return x+5

def func2(x,y,z):
	return x+2*y+3*z