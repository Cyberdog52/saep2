def main(x): # Does not work
    if(x): 
        return 1
    else: # Doesn't reach this. Solver won't try x = 0. Why?
        return 0

def expected_result():
    return [1,0]
