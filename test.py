def g(x):
	if x > 1:
		return 1
	else:
		return 0

def main(x):
	return g(x) + g(x)





'''
def g(x):
	return 1
	return 2
def main(x):
	return g(x)
'''
'''
def abs(v):
    if v >= 0:
        return v
    else:
        return -1 * v

def main(x):
    if (abs(x) == abs(-x)):
    	return True
    else:
    	return False
'''
'''
def g(x):
	if (x < 0):
		return -1
	else:
		return 1

def main(x,y):
	return g(x) + 1

'''
'''
def test(x, y):
    if (x != 0):
        return 1
    else:
        return 0



def main(x, y):
    return test(y,x)

def expected_result():
    return [0, 1]
'''
'''
def main(x, y):
	#y=3
	# x = 3 #assertion does not get triggered, if this is here
	#assert(x>5)
	if (y == 3):

		if (x < 2):

			return 0
		else:
			x=4
	else:
		return 8

	return x
'''