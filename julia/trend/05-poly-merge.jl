using CSV, DataFrames, Polynomials, Printf

function calc_coeff(df::DataFrame,
    x_col::Symbol, y_col::Symbol, order::Int)

  # Extract x and y values
  xs = df[!, x_col]
  ys = df[!, y_col]

  order_text = Dict(1 => "Linear",
    2 => "Quadratic", 3 => "Cubic")
  coeff_text = Dict(1 => "(a, b)",
    2 => "(a, b, c)", 3 => "(a, b, c, d)")

  # Perform polynomial fitting
  # Reverse coefficients to match output
  # Format coefficients
  pf = fit(xs, ys, order)
  cfs_r = reverse(coeffs(pf))
  cfs_fmt = [round(c, digits=2) for c in cfs_r]

  # Using string interpolation to print the result
  println("Curve type for $y_col: ",
    order_text[order])
  println("Coefficients ",
    "$(coeff_text[order]):\n\t$cfs_fmt\n")
end

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)

# Strip spaces from column names
rename!(df, Symbol.(strip.(string.(names(df)), ' ')))

# Call the function for each y column
# with respective order
println("Using Polynomials.fit\n")
calc_coeff(df, :xs, :ys1, 1)
calc_coeff(df, :xs, :ys2, 2)
calc_coeff(df, :xs, :ys3, 3)

