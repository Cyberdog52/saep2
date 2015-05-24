def main(x, y, z):
    x = 5

    y = z

    z = x

    y = 1

    z = z

    return x+y+z

def expected_result():
    return [11]