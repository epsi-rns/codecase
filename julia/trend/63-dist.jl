using StatsPlots, Distributions

# Generate data points for x-axis
x = range(-5, 5, length=1000)

# Calculate the corresponding y-values
# for a standard normal distribution
y = pdf(Normal(), x)

# Calculate the percentiles
percentiles = [25, 50, 75, 100]
quantiles = quantile.(Normal(), percentiles ./ 100)

# Plot the normal distribution
plot(
  x, y, fillrange = zero(x), fillalpha = 0.35,
  color=:black,
  label="Standard Normal Distribution", lw=1)
 
# Shade regions corresponding to percentiles
for (i, q) in enumerate(quantiles)
  sx = x .<= q
  sy = y[sx]
  # plot!(sx, sy, fillrange = zero(sx), fc=:blues)
  # vline!([q], color=i, alpha=0.3, label="")
end


# Add labels and title
xlabel!("x")
ylabel!("Density")
title!("Standard Normal Distribution with Quantiles")

# Save plot as PNG
savefig("63-quantiles.png")
