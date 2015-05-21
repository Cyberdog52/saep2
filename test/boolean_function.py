def main(x):
    if tester(x):
        return 0
    else:
        return 1


def tester(x):
    return (x == 0)


def expected_result():
    return [0, 1]
