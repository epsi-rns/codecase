import numpy as np

# Local Library
from Properties import get_properties, display

# Load properties from Properties.py helper
# and unpack them into local variables
properties = get_properties("50-samples.csv")
display(properties)
locals().update(properties)

# Calculate R-squared (R²)
r_squared = r_value ** 2

# Output of correlation calculation

print(f'sₓ (std dev)   = {x_std_dev:9.2f}')
print(f'sy (std dev)   = {y_std_dev:9.2f}')
print(f'r (pearson)    = {r_value:9.2f}')
print(f'R²             = {r_squared:9.2f}')
print()

# Create regression line
y_fit = m_slope * x_observed + b_intercept
y_err = y_observed - y_fit

# Calculate variance of residuals (MSE)
var_residuals = np.sum(y_err ** 2) / (n - 2)

# Calculate t-value
t_value = m_slope / std_err_slope

# Output the results
print(f'MSE = ∑ϵ²/(n-2)     = {var_residuals:9.2f}')
print(f'SE(β₁)  = √(MSE/sₓ) = {std_err_slope:9.2f}')
print(f't-value = β̅₁/SE(β₁) = {t_value:9.2f}')
print()

