# Read CSV file
pairCSV <- read.csv("50-samples.csv", header = TRUE)

# Extract x and y values from CSV data
x_observed <- pairCSV[, 1]
y_observed <- pairCSV[, 2]

# Number of data points
n <- length(x_observed)

# Calculate sums
x_sum <- sum(x_observed)
y_sum <- sum(y_observed)

# Calculate means
x_mean <- mean(x_observed)
y_mean <- mean(y_observed)

# Output of basic properties
cat(sprintf("%-10s = %4d\n", "n", n))
cat(sprintf("∑x (total) = %7.2f\n", x_sum))
cat(sprintf("∑y (total) = %7.2f\n", y_sum))
cat(sprintf("x̄ (mean)   = %7.2f\n", x_mean))
cat(sprintf("ȳ (mean)   = %7.2f\n\n", y_mean))

# Calculate deviations
x_deviation <- x_observed - x_mean
y_deviation <- y_observed - y_mean

# Calculate squared deviations
x_sq_deviation <- sum(x_deviation^2)
y_sq_deviation <- sum(y_deviation^2)

# Calculate cross-deviation
xy_cross_deviation <- sum(
  x_deviation * y_deviation)

# Calculate slope (m) and intercept (b)
m_slope <- lm(y_observed ~
  x_observed)$coefficients[2]
b_intercept <- lm(y_observed ~
  x_observed)$coefficients[1]

# Output of least square calculation
cat(sprintf("∑(xᵢ-x̄)    = %9.2f\n", sum(x_deviation)))
cat(sprintf("∑(yᵢ-ȳ)    = %9.2f\n", sum(y_deviation)))
cat(sprintf("∑(xᵢ-x̄)²   = %9.2f\n", x_sq_deviation))
cat(sprintf("∑(yᵢ-ȳ)²   = %9.2f\n", y_sq_deviation))
cat(sprintf("∑(xᵢ-x̄)(yᵢ-ȳ)  = %9.2f\n", xy_cross_deviation))
cat(sprintf("m (slope)      = %9.2f\n", m_slope))
cat(sprintf("b (intercept)  = %9.2f\n\n", b_intercept))

cat(sprintf("Equation     y = %5.2f + %5.2f.x\n\n", b_intercept, m_slope))

# Calculate variance
x_variance <- var(x_observed)
y_variance <- var(y_observed)

# Calculate covariance
xy_covariance <- cov(x_observed, y_observed)

# Calculate standard deviations
x_std_dev <- sd(x_observed)
y_std_dev <- sd(y_observed)

# Calculate Pearson correlation coefficient (r)
r <- cor(x_observed, y_observed)

# Calculate R-squared (R²)
r_squared <- r^2

# Output of correlation calculation
cat(sprintf("sₓ² (variance) = %9.2f\n", x_variance))
cat(sprintf("sy² (variance) = %9.2f\n", y_variance))
cat(sprintf("covariance     = %9.2f\n", xy_covariance))
cat(sprintf("sₓ (std dev)   = %9.2f\n", x_std_dev))
cat(sprintf("sy (std dev)   = %9.2f\n", y_std_dev))
cat(sprintf("r (pearson)    = %9.2f\n", r))
cat(sprintf("R²             = %9.2f\n\n", r_squared))

# Calculate residuals
residuals <- residuals(lm(y_observed ~ x_observed))

# Calculate sum of squared residuals
ss_residuals <- sum(residuals^2)

# Calculate degrees of freedom
df <- n - 2

# Calculate variance of residuals (MSE)
var_residuals <- ss_residuals / df

# Calculate standard error of the slope
std_err_slope <- sqrt(var_residuals / x_sq_deviation)

# Calculate t-value
t_value <- m_slope / std_err_slope

# Output the results
cat(sprintf("SSR = ∑ϵ²           = %9.2f\n", ss_residuals))
cat(sprintf("MSE = ∑ϵ²/(n-2)     = %9.2f\n", var_residuals))
cat(sprintf("SE(β₁)  = √(MSE/sₓ) = %9.2f\n", std_err_slope))
cat(sprintf("t-value = β̅₁/SE(β₁) = %9.2f\n", t_value))
