import numpy as np
import statistics

from scipy.stats import kurtosis, skew

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=int)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Number of data points
n = len(x_observed)

# Calculate maximum, minimum, and range
x_max = np.max(x_observed)
x_min = np.min(x_observed)
x_range = x_max - x_min

y_max = np.max(y_observed)
y_min = np.min(y_observed)
y_range = y_max - y_min

# Output of maximum, minimum, and range
print('x (max, min, range) = '
 + f'({x_min:7.2f}, {x_max:7.2f}, {x_range:7.2f} )')
print('y (max, min, range) = '
 + f'({y_min:7.2f}, {y_max:7.2f}, {y_range:7.2f} )')
print()

def calc_median(data: np.array) -> float:
  # Sort the data
  sorted_data = np.sort(data)

  # Calculate the median
  n = len(sorted_data)
  if n % 2 == 1:
    # If odd number of data points
    median = sorted_data[n // 2]
  else:
    # If even number of data points
    median = (sorted_data[n // 2 - 1] \
           +  sorted_data[n // 2]) / 2
  
  return median

# Calculate additional propeties
x_median = calc_median(x_observed)
y_median = calc_median(y_observed)

x_mode = statistics.mode(x_observed)
y_mode = statistics.mode(y_observed)

# Output of additional propeties
print(f'x median       = {x_median:9.2f}')
print(f'y median       = {y_median:9.2f}')
print(f'x mode         = {x_mode:9.2f}')
print(f'y mode         = {y_mode:9.2f}')
print()

def calc_se_kurtosis(n):
  return np.sqrt( \
    (24 * n * (n - 2) * (n - 3)) \
    / ((n + 1) * (n + 3) * (n - 1) ** 2))

def calc_se_skewness(n):
  return np.sqrt( \
    (6 * n * (n - 1)) \
    / ((n - 2) * (n + 1) * (n + 3)))

def calc_se_kurtosis_gaussian(n):
  return np.sqrt( \
    (4 * n**2 * calc_se_skewness(n)**2) \
    / ((n - 3) * (n + 5)))

# Calculate kurtosis and skewness
x_kurtosis = kurtosis(x_observed)
y_kurtosis = kurtosis(y_observed)

x_skewness = skew(x_observed)
y_skewness = skew(y_observed)

print(f'x kurtosis     = {x_kurtosis:9.2f}')
print(f'y kurtosis     = {y_kurtosis:9.2f}')
print(f'x skewness     = {x_skewness:9.2f}')
print(f'y skewness     = {y_skewness:9.2f}')
print()

# number of data points
x_n = len(x_observed)
y_n = len(y_observed)

# Calculate SE kurtosis and SE skewness
x_se_kurtosis = calc_se_kurtosis_gaussian(x_n)
y_se_kurtosis = calc_se_kurtosis_gaussian(y_n)
x_se_skewness = calc_se_skewness(x_n)
y_se_skewness = calc_se_skewness(y_n)

print(f'x SE kurtosis  = {x_se_kurtosis:9.2f}')
print(f'y SE kurtosis  = {y_se_kurtosis:9.2f}')
print(f'x SE skewness  = {x_se_skewness:9.2f}')
print(f'y SE skewness  = {y_se_skewness:9.2f}')
print()
