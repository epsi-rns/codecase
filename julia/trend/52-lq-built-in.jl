using CSV, DataFrames, Printf, Statistics, GLM

# Read data from CSV file
pairCSV = CSV.read("50-samples.csv", DataFrame)

# Extract x and y values from CSV data
x_observed = pairCSV.x
y_observed = pairCSV.y

# Number of data points
n = size(pairCSV, 1)

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

# Fit a linear model
model = lm(@formula(y ~ x), pairCSV)

# Get coefficients
# Extract slope and intercept
coefs = coef(model)
m_slope = coefs[2]
b_intercept = coefs[1]

# Output of least square calculation
@printf("m (slope)      = %9.2f\n", m_slope)
@printf("b (intercept)  = %9.2f\n\n", b_intercept)
@printf("Equation     y = %.2f + %.2f.x\n\n", b_intercept, m_slope)

# Calculate variance
x_variance = var(x_observed)
y_variance = var(y_observed)

# Calculate covariance
xy_covariance = cov(x_observed, y_observed)

# Calculate standard deviations
x_std_dev = std(x_observed)
y_std_dev = std(y_observed)

# Calculate Pearson correlation coefficient (r)
r = cor(x_observed, y_observed)

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

# Generate predicted values
# Calculate residuals
y_fit = predict(model)
y_err = residuals(model)

# Calculate sum of squared residuals
ss_residuals = sum(y_err .^ 2)

# Calculate degrees of freedom
df = n - 2

# Calculate variance of residuals (MSE)
var_residuals = ss_residuals / df

# Calculate standard error of the slope
x_deviation = x_observed .- x_mean
x_sq_deviation = sum(x_deviation .^ 2)
std_err_slope = sqrt(var_residuals / x_sq_deviation)

# Calculate t-value
t_value = m_slope / std_err_slope

# Output the results
@printf("SSR = ∑ϵ²           = %9.2f\n", ss_residuals)
@printf("MSE = ∑ϵ²/(n-2)     = %9.2f\n", var_residuals)
@printf("∑(xᵢ-x̄)²            = %9.2f\n", x_sq_deviation)
@printf("SE(β₁)  = √(MSE/sₓ) = %9.2f\n", std_err_slope)
@printf("t-value = β̅₁/SE(β₁) = %9.2f\n\n", t_value)
