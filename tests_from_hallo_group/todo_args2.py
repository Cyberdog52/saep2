def main(x): # Does not work
    if(x== 1):
        return f() * x
    else:
        return -1

def f():
    return 2

def expected_result():
    return [2,-1]