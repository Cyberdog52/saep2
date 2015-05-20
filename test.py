def main(x, y):
	y = 3
	# x = 3 #assertion does not get triggered, if this is here
	assert(True)
	if (y == 3):
		if (x < 2):
			return 0
		else:
			return 3
	else:
		return 1

# def twice(v): 
# 	return v + v
# def main(x, y): 
# 	z = twice(y) 
# 	if (x == z):
# 		if (x > y + 10): 
# 			return -1
# 		return 1 
# 	return 0
