using CSV, DataFrames, Polynomials, Plots

# Read data from CSV file
# Strip spaces from column names
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)), ' ')))

# Extract columns from DataFrame
xs = df.xs
ys = df.ys3
println(xs, "\n", ys, "\n")

# Perform cubic regression for ys
pf = fit(xs, ys, 3)
cfs_r = reverse(coeffs(pf))
cfs_fmt = [
  round(c, digits=2) for c in cfs_r]

println("Coefficients (a, b, c, d) for ys:")
println(cfs_fmt, "\n")

# Generate Series for Plotting
xp = range(minimum(xs), maximum(xs), length=100)
yp = pf.(xp)

# Plotting
scatter(xs, ys,
  label="Data Points")
plot!(xp, yp, color=:red,
  label="Fitted third-order polynomial")
xlabel!("X values")
ylabel!("Y values")
title!("Cubic curve fitting")

# Save the plot as a PNG file
savefig("13-poly-cubic.png")
