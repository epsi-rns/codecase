using CSV, DataFrames, Polynomials, Plots, Printf

mutable struct CurveFitter
  df::DataFrame
  x_col::Symbol
  y_cols::Vector{Symbol}

  function CurveFitter(df::DataFrame,
      x_col::Symbol, y_cols::Vector{Symbol})
    return new(df, x_col, y_cols)
  end
end

function calc_coeff(cf::CurveFitter,
    y_col::Symbol, order::Int)

  # Extract x and y values
  xs = cf.df[!, cf.x_col]
  ys = cf.df[!, y_col]

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
    coeff_text[order], ":\n\t", cfs_fmt, "\n")
end

function calc_coeffs(cf::CurveFitter, orders::Vector{Int})
  println("Using Polynomials.fit\n")
  for (y_col, order) in zip(cf.y_cols, orders)
      calc_coeff(cf, y_col, order)
  end
end

function calc_plot_all(cf::CurveFitter, y_col::Symbol)
  # Extract x and y values
  xs = cf.df[!, cf.x_col]
  ys = cf.df[!, y_col]

  # Generate x values for plotting
  xp = range(minimum(xs), maximum(xs), length=100)

  # Perform polynomial fitting for different orders
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
  savefig("16-poly-struct.png")
end

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)), ' ')))

# Define a CurveFitter object
# Specify the orders for each y_col
cf = CurveFitter(df, :xs, [:ys1, :ys2, :ys3])
orders = [1, 2, 3]

# Calculate coefficients and plot all three series
calc_coeffs(cf, orders)
calc_plot_all(cf, :ys3)
