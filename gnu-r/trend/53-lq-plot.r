# Load required libraries
library(ggplot2)

# Read CSV file
pairCSV <- read.csv("50-samples.csv", header = TRUE)

# Extract x and y values from CSV data
x_observed <- pairCSV[, 1]
y_observed <- pairCSV[, 2]

# Create a data frame with x and y observed values
data <- data.frame(x_observed, y_observed)

# Create a scatter plot of the observed data points
scatter_plot <- ggplot(
    data,
    aes(x = x_observed, y = y_observed),
    linewidth = 0.2) +
  geom_point(size = 0.5) +
  labs(x = "x", y = "y",
    title = "Scatter Plot of Observed Data") +
  theme_minimal() +
  theme(
    text = element_text(size = 4),
    plot.background = element_rect(fill = "white")) 

# Calculate slope (m) and intercept (b)
m_slope <- lm(y_observed ~
  x_observed)$coefficients[2]
b_intercept <- lm(y_observed ~
  x_observed)$coefficients[1]

# Calculate regression line
regression_line <- geom_abline(
  intercept = b_intercept, slope = m_slope,
  color = "red")

# Combine scatter plot and regression line
plot <- scatter_plot + regression_line

# Save plot as PNG
ggsave("53-lq-plot.png", plot,
  width = 800, height = 400, units = "px")