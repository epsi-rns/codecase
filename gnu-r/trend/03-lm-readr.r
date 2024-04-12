library(readr)

# Read data from CSV file
data <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Retrieve column specifications
column_spec <- spec(data)

# Extract x_values and y_values
x_values <- data$xs
y_values <- data$ys3

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