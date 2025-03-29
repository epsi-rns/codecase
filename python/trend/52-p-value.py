import numpy as np
from scipy.stats import linregress
from scipy.stats import t as t_distribution

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=float)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Number of data points
n = len(x_observed)

# Calculate slope (m), intercept (b),
# and other regression parameters
m_slope, b_intercept, r_value, p_value, \
std_err_slope = linregress(x_observed, y_observed)

# Create regression line
y_fit = m_slope * x_observed + b_intercept
y_err = y_observed - y_fit

# Calculate degrees of freedom
df = n - 2

# Calculate variance of residuals (MSE)
var_residuals = np.sum(y_err ** 2) / (n - 2)

# Calculate t-value
t_value = m_slope / std_err_slope

# Calculate two-tailed p-value
p_value = 2 * (1 - t_distribution.cdf(abs(t_value), df))

# Output the results
print(f'Slope (m): {m_slope:.2f}')
print(f'Standard error of the slope: {std_err_slope:.2f}')
print(f't-value: {t_value:.2f}')
print(f'Two-tailed p-value: {p_value:.10f}')
print()

# Define the significance level (alpha)
alpha = 0.05  # for a two-tailed test

# Calculate critical t-value
critical_t = t_distribution.ppf(1 - alpha / 2, df)

# Calculate the p-value manually
td = t_distribution.cdf(abs(t_value), df)
if abs(t_value) > critical_t:
  p_value_manual = 2 * (1 - td)
else:
  p_value_manual = 2 * td

print(f'Critical t-value: {critical_t:.10f}')
print(f'Manually calculated p-value: {p_value_manual:.10f}')

