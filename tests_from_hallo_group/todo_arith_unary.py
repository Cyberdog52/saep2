def main(x):
    assert(-x == 0 - x)
    assert(-x == -1 * x)
    assert((not True) == False)
    assert((not not True) == True)
    return -1

def expected_result():
    return [-1]
