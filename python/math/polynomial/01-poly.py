import numpy as np

order = 3
mx  = np.array([
        0, 1, 2, 3,
        4, 5, 6, 7,
        8, 9, 10, 11, 12])

mA = np.array([ 
       [(x ** i) for i in range(order+1)]
         for x in mx])

print(mA)
