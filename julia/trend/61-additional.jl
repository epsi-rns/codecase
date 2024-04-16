using CSV, DataFrames, Statistics, Printf, Distributions

# Read CSV file
pairCSV = CSV.read("50-samples.csv", DataFrame)

# Extract x and y values from CSV data
x_observed = pairCSV.x
y_observed = pairCSV.y

# Number of data points
n = length(x_observed)

# Calculate maximum, minimum, and range
x_max = maximum(x_observed)
x_min = minimum(x_observed)
x_range = x_max - x_min

y_max = maximum(y_observed)
y_min = minimum(y_observed)
y_range = y_max - y_min

# Output of maximum, minimum, and range
@printf("x (max, min, range) = (%7.2f, %7.2f, %7.2f)\n",
  x_min, x_max, x_range)
@printf("y (max, min, range) = (%7.2f, %7.2f, %7.2f)\n\n",
  y_min, y_max, y_range)

# Calculate median
x_median = median(x_observed)
y_median = median(y_observed)

# Calculate mode
x_mode = mode(x_observed)
y_mode = mode(y_observed)

# Output of additional properties
@printf("x median         = %9.2f\n", x_median)
@printf("y median         = %9.2f\n", y_median)
@printf("x mode           = %9.2f\n", x_mode)
@printf("y mode           = %9.2f\n\n", y_mode)
