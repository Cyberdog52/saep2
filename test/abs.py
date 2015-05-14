def abs(v):
    if v >= 0:
        return v
    else:
        return -1 * v

def main(x):
    assert( abs(x) >= 0 and abs(x) == abs(-x))
    return 0