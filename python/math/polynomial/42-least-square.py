import numpy as np

# Given data
x_values = np.array(
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y_values = np.array(
  [5, 12, 25, 44, 69, 100, 137,
    180, 229, 284, 345, 412, 485])

# Number of data points
n = len(x_values)

# Calculate sums
sum_x = np.sum(x_values)
sum_y = np.sum(y_values)

# Calculate means
mean_x = np.mean(x_values)
mean_y = np.mean(y_values)

# Output of basic properties
print(f'f{"n":1s} = {n:5d}')
print(f'∑x (total) = {sum_x:7.2f}')
print(f'∑y (total) = {sum_y:7.2f}')
print(f'x̄ (mean)   = {mean_x:7.2f}')
print(f'ȳ (mean)   = {mean_y:7.2f}')
print()

# Calculate deviations
deviation_x = x_values - mean_x
deviation_y = y_values - mean_y

# Calculate squared deviations
sq_deviation_x = np.sum(deviation_x ** 2)

# Calculate cross-deviation
cross_deviation_xy = np.sum(deviation_x * deviation_y)

# Calculate slope (m) and intercept (b)
slope_m = cross_deviation_xy / sq_deviation_x
intercept_b = mean_y - slope_m * mean_x

print('Manual Calculation')
print(f'Coefficients (b = {intercept_b:2,.2f},'
    + f' m = {slope_m:2,.2f})\n')
