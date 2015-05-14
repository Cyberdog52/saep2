def twice(v):
    return v + v


def test(x, y):
    z = twice(y)
    if (x == z):
        if (x > y + 10):
            return -1
        return 1
    return 0


def main(x, y):
    return test(x, y)

def expected_result():
    return [0, -1, 1]