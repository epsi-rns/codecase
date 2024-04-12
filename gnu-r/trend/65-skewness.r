# Load required libraries
library(ggplot2)

# Generate data points for x-axis
x <- seq(-5, 5, length.out = 1000)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard <- dnorm(x)

# Examples of distributions
# with different skewness parameters

# Negative skewness
y_skewed_1 <- dnorm(x) * 2 * pnorm(x)

# Moderate positive skewness
y_skewed_2 <- dnorm(x) * 2 * pnorm(-x)

# High positive skewness
y_skewed_3 <- dnorm(x) * 2 * pnorm(x) * 2

# Create data frames for plotting
df_standard <- data.frame(x = x, y = y_standard)
df_skewed_1 <- data.frame(x = x, y = y_skewed_1)
df_skewed_2 <- data.frame(x = x, y = y_skewed_2)
df_skewed_3 <- data.frame(x = x, y = y_skewed_3)

# Plot the normal distribution and skewed distributions
plot <- ggplot() +
  geom_line(data = df_standard, color = "black",
    aes(x = x, y = y), linewidth = 0.2) +
  geom_line(data = df_skewed_1,
    aes(x = x, y = y), color = "red",
    linetype = "dashed", linewidth = 0.2) +
  geom_line(data = df_skewed_2,
    aes(x = x, y = y), color = "green",
    linetype = "dashed", linewidth = 0.2) +
  geom_line(data = df_skewed_3,
    aes(x = x, y = y), color = "blue",
    linetype = "dashed", linewidth = 0.2) +
  labs(x = "x", y = "Density",
    title = "Normal Distribution with Different Skewness") +
  scale_linetype_manual(
    values = c("solid", "dashed", "dashed", "dashed"),
    labels = c(
      "Standard Normal",
      "Negative Skewness = -4",
      "Moderate Positive Skewness = 2",
      "High Positive Skewness = 6")) +
  theme_minimal() +
  theme(
    text = element_text(size = 4))

# Save plot as PNG
ggsave("65-skewness.png", plot,
  width = 800, height = 400, units = "px")
