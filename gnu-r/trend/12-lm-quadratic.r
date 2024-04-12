# Given data
x_values <- c(
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
y_values <- c(
  5, 12, 25, 44, 69, 100, 137,
  180, 229, 284, 345, 412, 485)

# Curve Fitting Order
order <- 2

# Perform quadratic regression using lm()
lm_model <- lm(y_values ~
  poly(x_values, order, raw = TRUE))

# Coefficients
coefficients <- coef(lm_model)

# Reverse order to match output
coefficients <- coefficients[
  length(coefficients):1]

# Print coefficients
cat("Coefficients (a, b, c):\n\t",
  coefficients, "\n")

# Open PNG graphics device
png("12-lm-quadratic.png", width = 800, height = 400)

# Draw Plot
plot(
  x_values, y_values, 
  xlab = "x", ylab = "y", 
  main = "Quadratic curve fitting", 
  pch = 16, col = "blue", 
  ylim = c(min(y_values), max(y_values)))

# Generate values for the quadratic curve
x_plot <- seq(
  min(x_values), max(x_values),
  length.out = 100)
y_plot <- predict(
  lm_model,
  newdata = data.frame(x_values = x_plot))

# Add quadratic curve
lines(x_plot, y_plot, col = "red")

# Add legend
legend("topleft",
  legend = c("Data points", "Quadratic Curve"), 
  col = c("blue", "red"),
  pch = c(16, NA), lty = c(NA, 1))
