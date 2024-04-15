# Load required libraries
library(ggplot2)

# Generate data points for x-axis
x <- seq(-5, 5, length.out = 1000)

# Calculate the corresponding y-values
# for a standard normal distribution
y <- dnorm(x)

# Create data frame for plotting
df <- data.frame(x = x, y = y)

# Calculate the percentiles
percentiles <- c(25, 50, 75, 100)
quantiles <- quantile(
  x, probs = percentiles / 100)

# Plot the normal distribution
plot <- ggplot(df, aes(x = x, y = y)) +
  geom_line(color = "black")

# Shade regions corresponding to percentiles
for (i in seq_along(quantiles)) {
  plot <- plot + geom_area(
    data = subset(df,x <= quantiles[i]),
    aes(x = x, y = y),
    fill = i, alpha = 0.3)
}

# Show grid
plot <- plot +
  theme_minimal() +
  theme(
    text = element_text(size = 4),
    plot.background = element_rect(fill = "white"),
    panel.grid = element_blank()) + 

  # Add labels and title
  labs(
    x = "x", y = "Density",
    title = "Standard Normal ",
      "Distribution with Quantiles")

# Save plot as PNG
ggsave("63-quantiles.png", plot,
  width = 800, height = 400, units = "px")
