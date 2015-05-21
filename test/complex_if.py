def main(x, y):
    if x < 0:
        return 0
    else:
        if x < 10:
            return 5
        elif x < 20:
            return 15

    return -1

def expected_result():
    return [0, 5, 15, -1]
