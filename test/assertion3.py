def main(x, y):
    # Assertion should pass
    assert(test(x,y) == test(y,x))
    return 1


def test(x, y):
    return x+y
