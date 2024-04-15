# Given data
x_values <- c(
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
y_values <- c(
  5, 14, 41, 98, 197, 350, 569, 866, 
  1253, 1742, 2345, 3074, 3941)

# Curve Fitting Order
order <- 3

# Perform cubic regression using lm()
lm_model <- lm(y_values ~
  poly(x_values, order, raw = TRUE))

# Coefficients
coefficients <- coef(lm_model)

# Reverse order to match output
coefficients <- coefficients[
  length(coefficients):1]

# Print coefficients
cat("Coefficients (a, b, c, d):\n\t",
  coefficients, "\n")

