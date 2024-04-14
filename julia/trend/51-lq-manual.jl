using CSV, DataFrames, Printf, Statistics

# Read data from CSV file
pairCSV = CSV.read("50-samples.csv", DataFrame)

# Extract x and y values from CSV data
x_observed = pairCSV.x
y_observed = pairCSV.y

# Number of data points
n = length(x_observed)

# Calculate sums
x_sum = sum(x_observed)
y_sum = sum(y_observed)

# Calculate means
x_mean = mean(x_observed)
y_mean = mean(y_observed)

# Output of basic properties
@printf("%-10s = %4d\n", "n", n)
@printf("∑x (total) = %7.2f\n", x_sum)
@printf("∑y (total) = %7.2f\n", y_sum)
@printf("x̄ (mean)   = %7.2f\n", x_mean)
@printf("ȳ (mean)   = %7.2f\n\n", y_mean)

# Calculate deviations
x_deviation = x_observed .- x_mean
y_deviation = y_observed .- y_mean

# Calculate squared deviations
x_sq_deviation = sum(x_deviation .^ 2)
y_sq_deviation = sum(y_deviation .^ 2)

# Calculate cross-deviation
xy_cross_deviation = sum(x_deviation .* y_deviation)

# Calculate slope (m) and intercept (b)
m_slope = xy_cross_deviation / x_sq_deviation
b_intercept = y_mean - m_slope * x_mean

# Output of least square calculation
@printf("∑(xᵢ-x̄)    = %9.2f\n", sum(x_deviation))
@printf("∑(yᵢ-ȳ)    = %9.2f\n", sum(y_deviation))
@printf("∑(xᵢ-x̄)²   = %9.2f\n", x_sq_deviation)
@printf("∑(yᵢ-ȳ)²   = %9.2f\n", y_sq_deviation)
@printf("∑(xᵢ-x̄)(yᵢ-ȳ)  = %9.2f\n", xy_cross_deviation)
@printf("m (slope)      = %9.2f\n", m_slope)
@printf("b (intercept)  = %9.2f\n\n", b_intercept)

@printf("Equation     y = %.2f + %.2f.x\n\n", b_intercept, m_slope)

# Calculate variance
x_variance = x_sq_deviation / (n-1)
y_variance = y_sq_deviation / (n-1)

# Calculate covariance
xy_covariance = xy_cross_deviation / (n-1)

# Calculate standard deviations
x_std_dev = sqrt(x_variance)
y_std_dev = sqrt(y_variance)

# Calculate Pearson correlation coefficient (r)
r = xy_covariance / (x_std_dev * y_std_dev)

# Calculate R-squared (R²)
r_squared = r^2

# Output of correlation calculation
@printf("sₓ² (variance) = %9.2f\n", x_variance)
@printf("sy² (variance) = %9.2f\n", y_variance)
@printf("covariance     = %9.2f\n", xy_covariance)
@printf("sₓ (std dev)   = %9.2f\n", x_std_dev)
@printf("sy (std dev)   = %9.2f\n", y_std_dev)
@printf("r (pearson)    = %9.2f\n", r)
@printf("R²             = %9.2f\n\n", r_squared)

# Create regression line
y_fit = m_slope .* x_observed .+ b_intercept
y_err = y_observed .- y_fit

# Calculate sum of squared residuals
ss_residuals = sum(y_err .^ 2)

# Calculate degrees of freedom
df = n - 2

# Calculate variance of residuals (MSE)
var_residuals = ss_residuals / df

# Calculate standard error of the slope
std_err_slope = sqrt(var_residuals / x_sq_deviation)

# Calculate t-value
t_value = m_slope / std_err_slope

# Output the results
@printf("SSR = ∑ϵ²           = %9.2f\n", ss_residuals)
@printf("MSE = ∑ϵ²/(n-2)     = %9.2f\n", var_residuals)
@printf("SE(β₁)  = √(MSE/sₓ) = %9.2f\n", std_err_slope)
@printf("t-value = β̅₁/SE(β₁) = %9.2f\n\n", t_value)
