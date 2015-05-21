def test(x, y):
    if (x != 0):
	    return 1
    else:
        return 0
	


def main(x, y):
    return test(test(y,x), y)

def expected_result():
    return [0, 1]
