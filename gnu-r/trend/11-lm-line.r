# Given data
x_values <- c(
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
y_values <- c(
  5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53)

# Curve Fitting Order
order <- 1

# Perform linear regression using lm()
lm_model <- lm(y_values ~ 
  poly(x_values, order, raw = TRUE))

# Coefficients
coefficients <- coef(lm_model)

# Reverse order to match output
coefficients <- coefficients[
  length(coefficients):1]

# Print coefficients
cat("Coefficients (a, b):\n\t",
  coefficients, "\n")

# Open PNG graphics device
png("11-lm-line.png", width = 800, height = 400)

# Plot data points
plot(
  x_values, y_values,
  pch = 16, col = "blue",
  xlab = "x", ylab = "y",
  main = "Straight line fitting")

# Generate values for the regression line
x_plot <- seq(
  min(x_values), max(x_values),
  length.out = 100)
y_plot <- predict(
  lm_model,
  newdata = data.frame(x_values = x_plot))

# Add regression line
lines(x_plot, y_plot, col = "red")

# Add legend
legend("topright",
  legend = c("Data points", "Linear Equation"),
  col = c("blue", "red"),
  pch = c(16, NA), lty = c(NA, 1))
