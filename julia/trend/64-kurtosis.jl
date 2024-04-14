using StatsPlots, Distributions

# Generate data points for x-axis
x = range(-5, 5, length=1000)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard = pdf.(Normal(), x)

# Examples of distributions
# with different levels of kurtosis

# Standard normal distribution (Kurtosis = 0)
y_kurtosis_1 = pdf.(Normal(1, 1), x)

# Lower kurtosis
y_kurtosis_2 = pdf.(Normal(1, 0.5), x)

# Higher kurtosis
y_kurtosis_3 = pdf.(Normal(1, 2), x)

# Plot the normal distribution and
# distributions with different levels of kurtosis
plot(
  x, y_standard, color=:black,
  label="Standard Normal",
  title = "Normal Distribution "
    * "with Different Kurtosis",
  xlabel = "x", ylabel = "Density",
)

plot!(
  x, y_kurtosis_1, color=:red,
  label="Standard Kurtosis = 0",
  linestyle=:dash, 
)

plot!(
  x, y_kurtosis_2, color=:green,
  label="Lower Kurtosis",
  linestyle=:dash, 
)

plot!(
  x, y_kurtosis_3, color=:blue,
  label="Higher Kurtosis",
  linestyle=:dash, 
)

# Save plot as PNG
savefig("64-kurtosis.png")
