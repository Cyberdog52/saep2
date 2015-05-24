def main (x,y):

	b=1 or not 0 and True	#b=True
	if(x == 1):
		if (42): #42 is casted to 'True'
			return 0
	if (b and x<3):
		return 1
	if (not -(-1)):	#not reachable
		return -1
	else:
		r=(x==4 or y==4)

	if (r*r):
		return 2
	if(1*(y>4)):
		return 3
	if (not(not(1))): #always True
		return 4
	return 5 #not reachable

def expected_result():
  return [1,2,3,4,0]
	
