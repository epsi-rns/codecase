# Load required libraries
library(ggplot2)

# Generate data points for x-axis
x <- seq(-5, 5, length.out = 1000)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard <- dnorm(x)

# Examples of distributions
# with different levels of kurtosis

# Standard normal distribution (Kurtosis = 0)
y_kurtosis_1 <- dnorm(x, mean = 1, sd = 1)

# Lower kurtosis
y_kurtosis_2 <- dnorm(x, mean = 1, sd = 0.5)

# Higher kurtosis
y_kurtosis_3 <- dnorm(x, mean = 1, sd = 2)

# Create data frames for plotting
df_standard <- data.frame(x = x, y = y_standard)
df_kurtosis_1 <- data.frame(x = x, y = y_kurtosis_1)
df_kurtosis_2 <- data.frame(x = x, y = y_kurtosis_2)
df_kurtosis_3 <- data.frame(x = x, y = y_kurtosis_3)

# Plot the normal distribution and
# distributions with different levels of kurtosis
plot <- ggplot() +
  geom_line(data = df_standard, color = "black",
    aes(x = x, y = y), linewidth = 0.2) +
  geom_line(data = df_kurtosis_1,
    aes(x = x, y = y), color = "red",
    linetype = "dashed", linewidth = 0.2) +
  geom_line(data = df_kurtosis_2,
    aes(x = x, y = y), color = "green",
    linetype = "dashed", linewidth = 0.2) +
  geom_line(data = df_kurtosis_3,
    aes(x = x, y = y), color = "blue",
    linetype = "dashed", linewidth = 0.2) +
  labs(x = "x", y = "Density",
    title = "Normal Distribution ",
      "with Different Kurtosis") +
  scale_linetype_manual(
    values = c("solid", "dashed", "dashed", "dashed"),
    labels = c(
      "Standard Normal", "Standard Kurtosis = 0",
      "Lower Kurtosis", "Higher Kurtosis")) +
  theme_minimal() +
  theme(
    text = element_text(size = 4))

# Save plot as PNG
ggsave("64-kurtosis.png", plot,
  width = 800, height = 400, units = "px")
