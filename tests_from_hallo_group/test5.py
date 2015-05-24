def main(a,b,c,d,e):
	v=10
	ret=0
	if (a<b and b<c):
		assert a<c
		return 1
	if (a==1):
		assert a!=1
	elif (a>=1):
		if a==2:
			return 2
		else:
			ret=5
	else:
		ret=6

	if func(d,e):
		return 3

	ret=ret+v
	return ret

def func(x,y):
	assert x>y
	if (x>y):
		if(x==1):
			if(x==4):
				assert x==1
				return False
	return x<y

def expected_result():
  return [1,2,3,10,15,16]