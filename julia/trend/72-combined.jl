using CSV, DataFrames, Statistics, StatsPlots, ColorSchemes

# Read data from CSV file
df = CSV.read("series.csv", DataFrame, types=Dict())
rename!(df, Symbol.(strip.(string.(names(df)))))

# Extract x and y values from CSV data
xs = df.xs
ys1 = df.ys1
ys2 = df.ys2
ys3 = df.ys3

# Calculate standard error for each y series
se1 = std(ys1) / sqrt(length(ys1))
se2 = std(ys2) / sqrt(length(ys2))
se3 = std(ys3) / sqrt(length(ys3))

# Define color scheme for shading
colors = ColorSchemes.magma.colors

# Scatter plot with regression line for ys1
plot1 = scatter(
  xs, ys1, label="ys1",
  seriestype=:scatter, color=:red)
scatter!(
  xs, ys1, label="", color=:red)
plot!(
  xs, ys1, label="", color=colors[1],
  ribbon=(se1, se1), fillalpha=0.3)
xlabel!("x")
ylabel!("y")
title!(
  "Regression Line for y1",
  titlefontsize=8)

# Scatter plot with regression line for ys2
plot2 = scatter(
  xs, ys2, label="ys2",
  seriestype=:scatter, color=:green)
scatter!(
  xs, ys2, label="", color=:green)
plot!(
  xs, ys2, label="", color=colors[2],
  ribbon=(se2, se2), fillalpha=0.3)
xlabel!("x")
ylabel!("y")
title!(
  "Quadratic Regression Line for y2",
  titlefontsize=8)

# Scatter plot with regression line for ys3
plot3 = scatter(
  xs, ys3, label="ys3",
  seriestype=:scatter, color=:blue)
scatter!(
  xs, ys3, label="", color=:blue)
plot!(
  xs, ys3, label="", color=colors[3],
  ribbon=(se3, se3), fillalpha=0.3)
xlabel!("x")
ylabel!("y")
title!(
  "Cubic Regression Line for y3",
  titlefontsize=8)

# Combine plots into a single figure
plot_combined = plot(
  plot1, plot2, plot3, layout=(1, 3))

# Save plot as PNG
savefig("72-combined.png")
