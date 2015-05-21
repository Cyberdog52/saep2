def main(x, y):
    # Assertion should pass
    assert(test(x,y) == test(x, 0))
    return 1


def test(x, y):
    return x+y
