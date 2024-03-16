import numpy as np

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=float)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Number of data points
n = len(x_observed)

# Calculate sums
x_sum = np.sum(x_observed)
y_sum = np.sum(y_observed)

# Calculate means
x_mean = np.mean(x_observed)
y_mean = np.mean(y_observed)

# Output of basic properties
print(f'{f"n":10s} = {n:4d}')
print(f'∑x (total) = {x_sum:7.2f}')
print(f'∑y (total) = {y_sum:7.2f}')
print(f'x̄ (mean)   = {x_mean:7.2f}')
print(f'ȳ (mean)   = {y_mean:7.2f}')
print()

# Calculate deviations
x_deviation = x_observed - x_mean
y_deviation = y_observed - y_mean

# Calculate squared deviations
x_sq_deviation = np.sum(x_deviation ** 2)
y_sq_deviation = np.sum(x_deviation ** 2)

# Calculate cross-deviation
xy_cross_deviation = np.sum(x_deviation * y_deviation)
# Calculate slope (m) and intercept (b)
m_slope = xy_cross_deviation / x_sq_deviation
b_intercept = y_mean - m_slope * x_mean

# Output of least square calculation
print(f'∑(xᵢ-x̄)    = {np.sum(x_deviation):9.2f}')
print(f'∑(yᵢ-ȳ)    = {np.sum(y_deviation):9.2f}')
print(f'∑(xᵢ-x̄)²   = {x_sq_deviation:9.2f}')
print(f'∑(yᵢ-ȳ)²   = {y_sq_deviation:9.2f}')
print(f'∑(xᵢ-x̄)(yᵢ-ȳ)  = {xy_cross_deviation:9.2f}')
print(f'm (slope)      = {m_slope:9.2f}')
print(f'b (intercept)  = {b_intercept:9.2f}')
print()

print(f'Equation     y = ' \
  + f'{b_intercept:5.2f} + {m_slope:5.2f}.x')
print()

# Calculate variance
x_variance = x_sq_deviation / n
y_variance = y_sq_deviation / n

# Calculate covariance
xy_covariance = xy_cross_deviation / n

# Calculate standard deviations
x_std_dev = np.sqrt(x_variance)
y_std_dev = np.sqrt(y_variance)

# Calculate Pearson correlation coefficient (r)
r = xy_covariance / (x_std_dev * y_std_dev)

# Calculate R-squared (R²)
r_squared = r ** 2

# Output of correlation calculation
print(f'sₓ² (variance) = {x_variance:9.2f}')
print(f'sy² (variance) = {y_variance:9.2f}')
print(f'covariance     = {xy_covariance:9.2f}')
print(f'sₓ (std dev)   = {x_std_dev:9.2f}')
print(f'sy (std dev)   = {y_std_dev:9.2f}')
print(f'r (pearson)    = {r:9.2f}')
print(f'R²             = {r_squared:9.2f}')
print()

# Create regression line
y_fit = m_slope * x_observed + b_intercept
y_err = y_observed - y_fit

# Calculate sum of squared residuals
ss_residuals = np.sum(y_err ** 2)

# Calculate degrees of freedom
df = n - 2

# Calculate variance of residuals (MSE)
var_residuals = ss_residuals / df

# Calculate standard error of the slope
std_err_slope = np.sqrt(var_residuals / x_sq_deviation)

# Calculate t-value
t_value = m_slope / std_err_slope

# Output the results
print(f'SSR = ∑ϵ²           = {ss_residuals:9.2f}')
print(f'MSE = ∑ϵ²/(n-2)     = {var_residuals:9.2f}')
print(f'SE(β₁)  = √(MSE/sₓ) = {std_err_slope:9.2f}')
print(f't-value = β̅₁/SE(β₁) = {t_value:9.2f}')
print()
