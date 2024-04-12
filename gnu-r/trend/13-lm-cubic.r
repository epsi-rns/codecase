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

# Open PNG graphics device
png("13-lm-cubic.png", width = 800, height = 400)

# Draw Plot
plot(
  x_values, y_values, 
  xlab = "x", ylab = "y", 
  main = "Cubic curve fitting", 
  pch = 16, col = "blue", 
  ylim = c(min(y_values), max(y_values)))

# Generate values for the cubic curve
x_plot <- seq(
  min(x_values), max(x_values),
  length.out = 100)
y_plot <- predict(
  lm_model,
  newdata = data.frame(x_values = x_plot))

# Add cubic curve
lines(x_plot, y_plot, col = "red")

# Add legend
legend("topleft",
  legend = c("Data points", "Cubic Curve"), 
  col = c("blue", "red"),
  pch = c(16, NA), lty = c(NA, 1))
