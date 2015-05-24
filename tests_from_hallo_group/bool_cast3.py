def main(x):
    z = True
    if foo(z):
        return foo(z) + bar(z) # 1 + 2 = 3
    else:
        #Unreachable
        return 0

def foo(x):
    return x

def bar(x):
    return x + 1

def expected_result():
    return [3]

