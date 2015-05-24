

def main(x):
    if (x < 1):
        return 1
    elif (x >= 1):
        return 2
    else:
        y = 2   #Unreachable code
        z = 3
        a = foo(z+ y)
        assert (False)
        return 10

def foo(x):
    return x

def expected_result():
    return [1, 2]

