using StatsPlots, Distributions

# Generate data points for x-axis
x = range(-5, 5, length=1000)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard = pdf.(Normal(), x)

# Examples of distributions
# with different skewness parameters

# Negative skewness
y_skewed_1 = (2 * pdf.(Normal(), x) 
  .* cdf.(Normal(), x))

# Moderate positive skewness
y_skewed_2 = (2 * pdf.(Normal(), -x) 
  .* cdf.(Normal(), -x))

# High positive skewness
y_skewed_3 = (2 * pdf.(Normal(), x) 
  .* cdf.(Normal(), x) * 2)

# Plot the normal distribution
# and skewed distributions
plot(
  x, y_standard, color=:black,
label="Standard Normal",
  title = "Normal Distribution "
    * "with Different Skewness",
  xlabel = "x", ylabel = "Density",
)

plot!(
  x, y_skewed_1, color=:red,
  label="Negative Skewness = -4",
  linestyle=:dash,
)

plot!(
  x, y_skewed_2, color=:green,
  label="Moderate Positive Skewness = 2",
  linestyle=:dash,
)

plot!(
  x, y_skewed_3, color=:blue,
  label="High Positive Skewness = 6",
  linestyle=:dash,
)

# Save plot as PNG
savefig("65-skewness.png")
