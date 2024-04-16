using CSV, DataFrames, Plots, GLM

# Read data from CSV file
pairCSV = CSV.read("50-samples.csv", DataFrame)

# Extract x and y values from CSV data
x_observed = pairCSV.x
y_observed = pairCSV.y

# Create a scatter plot of the observed data points
scatter_plot = scatter(
  x_observed, y_observed,
  xlabel = "x", ylabel = "y",
  title = "Scatter Plot of Observed Data",
  markersize = 2,
  legend = false,
  color = :blue,
  grid = false,
  size = (800, 400))

# Fit a linear model
model = lm(@formula(y ~ x), pairCSV)

# Get coefficients
# Extract slope and intercept
coefs = coef(model)
m_slope = coefs[2]
b_intercept = coefs[1]

# Calculate regression line
regression_line = plot!(
  x -> m_slope * x + b_intercept,
  xlims = extrema(x_observed),
  color = :red, linewidth = 2)

# Save plot as PNG
savefig("55-lq-plot.png")
