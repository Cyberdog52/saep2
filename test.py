'''
def main(x):
	return 5
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
#'''
def test(x, y):
    if (x != 0):
        return 1
    else:
        return 0



def main(x, y):
    return test(y,x)

def expected_result():
    return [0, 1]
#'''
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
'''

# def twice(v): 
# 	return v + v
# def main(x, y): 
# 	z = twice(y) 
# 	if (x == z):
# 		if (x > y + 10): 
# 			return -1
# 		return 1 
# 	return 0

'''
