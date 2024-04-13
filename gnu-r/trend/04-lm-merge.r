calc_coeff <- function(x_values, y_values, order) {
  # Perform linear regression using lm()
  lm_model <- lm(y_values ~ 
    poly(x_values, order, raw = TRUE))

  # Define a named vector
  # to map order numbers to curve types
  coeff_text <- c(
    "(a, b)" = 1, "(a, b, c)" = 2, "(a, b, c, d)" = 3)
  order_text <- c(
    "Linear" = 1, "Quadratic" = 2, "Cubic" = 3)

  # Print the curve type
  cat(paste("Using lm_model :",
    names(order_text)[order], "\n"))

  # Coefficients
  coefficients <- coef(lm_model)

  # Reverse order to match output
  coefficients <- coefficients[
    length(coefficients):1]

  # Print coefficients
  cat("Coefficients ",
    names(coeff_text)[order], ":\n\t",
    coefficients, "\n")
}

# Load required library
library(readr)

# Read data from CSV file
data <- read_csv(
  "series.csv",
  show_col_types = FALSE)

calc_coeff(data$xs, data$ys1, 1)
calc_coeff(data$xs, data$ys2, 2)
calc_coeff(data$xs, data$ys3, 3)

