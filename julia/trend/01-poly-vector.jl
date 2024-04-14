using Polynomials

# Given data
x_values = [
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
y_values = [
  5, 9, 13, 17, 21, 25, 29,
  33, 37, 41, 45, 49, 53]

# Curve Fitting Order
order = 1

# Perform linear regression using Polynomials.fit
pf = fit(x_values, y_values, order)
println("Using Polynomials.fit")

# Extract coefficients and reverse them
coeffs_r= reverse(coeffs(pf)) 
println("Coefficients (a, b):")

# Format coefficients
coeffs_fmt = [
  round(c, digits=2) for c in coeffs_r]  
println(coeffs_fmt, "\n")

