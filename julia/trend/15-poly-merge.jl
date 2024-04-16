using CSV, DataFrames, Polynomials, Plots, Printf

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

function calc_coeffs(df::DataFrame)
  # Call the function for each y column
  # with respective order
  println("Using Polynomials.fit\n")

  calc_coeff(df, :xs, :ys1, 1)
  calc_coeff(df, :xs, :ys2, 2)
  calc_coeff(df, :xs, :ys3, 3)
end

function calc_plot_all(df::DataFrame,
    x_col::Symbol, y_col::Symbol)

  # Extract x and y values
  xs = df[!, x_col]
  ys = df[!, y_col]

  # Draw Plot
  xp = range(minimum(xs), maximum(xs), length=100)
  yp1 = fit(xs, ys, 1).(xp)
  yp2 = fit(xs, ys, 2).(xp)
  yp3 = fit(xs, ys, 3).(xp)

  # Plotting
  scatter(xs, ys,
    label="Data Points")
  plot!(xp, yp1, color=:red,
    label="Linear Equation")
  plot!(xp, yp2, color=:green,
    label="Fitted second-order polynomial")
  plot!(xp, yp3, color=:blue,
    label="Fitted third-order polynomial")

  # Decoration
  xlabel!("X values")
  ylabel!("Y values")
  title!("Polynomial Curve Fitting")

  # Save the plot as a PNG file
  savefig("15-poly-merge.png")
end

# Read data from CSV file
# Strip spaces from column names
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Plot all three series
calc_coeffs(df)
calc_plot_all(df, :xs, :ys3)


