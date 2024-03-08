import numpy as np

order = 3
mx  = np.array([
        0, 1, 2, 3,
        4, 5, 6, 7,
        8, 9, 10, 11, 12])
mB  = np.array([
         5,   14,   41,   98,
       197,  350,  569,  866,
      1253, 1742, 2345, 3074, 3941])

mA = np.array([ 
       [(x ** i) for i in range(order+1)]
         for x in mx])

mAt   = np.transpose(mA)
mAt_A = np.matmul(mAt, mA)
mAt_B = np.matmul(mAt, mB)

# First Method
mAt_A_i = np.linalg.inv(mAt_A)
mC      = np.matmul(mAt_A_i, mAt_B)
print("Coefficients (a, b, c, d):", mC)

# Second Method
mC      = np.linalg.solve(mAt_A, mAt_B)
print("Coefficients (a, b, c, d):", mC)
