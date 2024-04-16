using CSV, DataFrames, Printf, Statistics, GLM

# Read data from CSV file
df = CSV.read("50-samples.csv", DataFrame)

# Extract x and y values from CSV data
xᵢ = df.x
yᵢ = df.y

# Number of data points
n = length(xᵢ)

# Calculate sums
∑x = sum(xᵢ)
∑y = sum(yᵢ)

# Calculate means
x̄ = mean(xᵢ)
ȳ = mean(yᵢ)

# Output of basic properties
@printf("%-10s = %4d\n", "n", n)
@printf("∑x (total) = %7.2f\n", ∑x)
@printf("∑y (total) = %7.2f\n", ∑y)
@printf("x̄ (mean)   = %7.2f\n", x̄)
@printf("ȳ (mean)   = %7.2f\n\n", ȳ)

# Calculate variance
sₓ² = sum((xᵢ .- x̄).^2) / (n - 1)
sʸ² = sum((yᵢ .- ȳ).^2) / (n - 1)

# Calculate covariance
cov = sum((xᵢ .- x̄) .* (yᵢ .- ȳ)) / (n - 1)

# Calculate standard deviations
sₓ = sqrt(sₓ²)
sʸ = sqrt(sʸ²)

# Calculate Pearson correlation coefficient (r)
r = cov / (sₓ * sʸ)

# Calculate R-squared (R²)
r² = r^2

# Output of correlation calculation
@printf("sₓ² (variance) = %9.2f\n", sₓ²)
@printf("sʸ² (variance) = %9.2f\n", sʸ²)
@printf("covariance     = %9.2f\n", cov)
@printf("sₓ (std dev)   = %9.2f\n", sₓ)
@printf("sʸ (std dev)   = %9.2f\n", sʸ)
@printf("r (pearson)    = %9.2f\n", r)
@printf("R²             = %9.2f\n\n", r²)

# Calculate slope (m) and intercept (b)
mᵣ = sum((xᵢ .- x̄) .* (yᵢ .- ȳ)) / sum((xᵢ .- x̄).^2)
bᵣ = ȳ - mᵣ * x̄

@printf("m (slope)      = %9.2f\n", mᵣ)
@printf("b (intercept)  = %9.2f\n\n", bᵣ)
@printf("Equation     y = %.2f + %.2f.x\n\n", bᵣ, mᵣ)

# Create regression line
ŷᵢ = mᵣ .* xᵢ .+ bᵣ
ϵᵢ = yᵢ .- ŷᵢ

# Calculate sum of squared residuals
∑ϵ² = sum(ϵᵢ .^ 2)

# Calculate degrees of freedom
df = n - 2

# Calculate variance of residuals (MSE)
MSE = ∑ϵ² / df

# Calculate standard error of the slope
SE_β₁ = sqrt(MSE / sum((xᵢ .- x̄).^2))

# Calculate t-value
tᵥ = mᵣ / SE_β₁

# Output the results
@printf("SSR = ∑ϵ²           = %9.2f\n", ∑ϵ²)
@printf("MSE = ∑ϵ²/(n-2)     = %9.2f\n", MSE)
@printf("SE(β₁)  = √(MSE/sₓ) = %9.2f\n", SE_β₁)
@printf("t-value = β̅₁/SE(β₁) = %9.2f\n\n", tᵥ)
