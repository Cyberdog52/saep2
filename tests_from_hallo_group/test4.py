def main (x,y):

	s=func(2)
	return s

def func(x):
	if (x+(True and False)): #if(2) is True
		return 5
	else:			#not reachable
		return x+5