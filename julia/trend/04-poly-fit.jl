using CSV, DataFrames, Polynomials, Printf

# Read data from CSV file
# Strip spaces from column names
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Extract columns from DataFrame
x_values = df.xs
y_values1 = df.ys1
y_values2 = df.ys2
y_values3 = df.ys3

# Perform linear regression for ys1
pf_1 = fit(x_values, y_values1, 1)

coeffs_r1 = reverse(coeffs(pf_1))
coeffs_fmt_1 = [
  round(c, digits=2) for c in coeffs_r1]

println("Coefficients (a, b) for ys1:")
println(coeffs_fmt_1, "\n")

# Perform quadratic curve fitting for ys2
pf_2 = fit(x_values, y_values2, 2)

coeffs_r2 = reverse(coeffs(pf_2))
coeffs_fmt_2 = [
  round(c, digits=2) for c in coeffs_r2]

println("Coefficients (a, b, c) for ys2:")
println(coeffs_fmt_2, "\n")

# Perform cubic curve fitting for ys3
pf_3 = fit(x_values, y_values3, 3)

coeffs_r3 = reverse(coeffs(pf_3))
coeffs_fmt_3 = [
  round(c, digits=2) for c in coeffs_r3]

println("Coefficients (a, b, c, d) for ys3:")
println(coeffs_fmt_3, "\n")

