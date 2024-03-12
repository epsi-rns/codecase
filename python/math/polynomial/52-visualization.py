import numpy as np
import matplotlib.pyplot as plt

# Numpy setup
np.set_printoptions(
  precision=2,
  formatter={
    'int':   '{:30,d}'.format,
    'float': '{:10,.8f}'.format
  },
  linewidth=np.inf,
  suppress=True)

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=float)
  
# Extract x and y values from CSV data
x_values = pairCSV[:, 0]
y_values = pairCSV[:, 1]

# Number of data points
n = len(x_values)

# Calculate sums
sum_x = np.sum(x_values)
sum_y = np.sum(y_values)

# Calculate means
mean_x = np.mean(x_values)
mean_y = np.mean(y_values)

# Calculate deviations
deviation_x = x_values - mean_x
deviation_y = y_values - mean_y

# Calculate squared deviations
sq_deviation_x = np.sum(deviation_x ** 2)
sq_deviation_y = np.sum(deviation_y ** 2)

# Calculate cross-deviation
cross_deviation_xy = np.sum(deviation_x * deviation_y)

# Calculate variance
variance_x = sq_deviation_x / n
variance_y = sq_deviation_y / n

# Calculate covariance
covariance_xy = cross_deviation_xy / n

# Calculate slope (m) and intercept (b)
slope_m = cross_deviation_xy / sq_deviation_x
intercept_b = mean_y - slope_m * mean_x

# Calculate standard deviations
std_dev_x = np.sqrt(variance_x)
std_dev_y = np.sqrt(variance_y)

# Calculate Pearson correlation coefficient (r)
r = covariance_xy / (std_dev_x * std_dev_y)

# Calculate R-squared (R²)
r_squared = r ** 2

# Output the results
print(f'{f"n":10s} = {n:4d}')
print(f'∑x (total) = {sum_x:7.2f}')
print(f'∑y (total) = {sum_y:7.2f}')
print(f'x̄ (mean)   = {mean_x:7.2f}')
print(f'ȳ (mean)   = {mean_y:7.2f}')
print(f'∑(xᵢ-x̄)    = {np.sum(deviation_x):9.2f}')
print(f'∑(yᵢ-ȳ)    = {np.sum(deviation_y):9.2f}')
print(f'∑(xᵢ-x̄)²       = {sq_deviation_x:9.2f}')
print(f'∑(yᵢ-ȳ)²       = {sq_deviation_y:9.2f}')
print(f'∑(xᵢ-x̄)(yᵢ-ȳ)  = {cross_deviation_xy:9.2f}')
print(f'm (slope)      = {slope_m:9.2f}')
print(f'b (intercept)  = {intercept_b:9.2f}')
print(f'sₓ² (variance) = {variance_x:9.2f}')
print(f'sy² (variance) = {variance_y:9.2f}')
print(f'covariance     = {covariance_xy:9.2f}')
print(f'sₓ (std dev)   = {std_dev_x:9.2f}')
print(f'sy (std dev)   = {std_dev_y:9.2f}')
print(f'r (pearson)    = {r:9.2f}')
print(f'R²             = {r_squared:9.2f}')

# Create regression line
regression_line_y = slope_m * x_values + intercept_b

# Plot the data and regression line
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values, color='blue', label='Data Points')
plt.plot(x_values, regression_line_y, color='red', label='Regression Line')
plt.title('Linear Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
