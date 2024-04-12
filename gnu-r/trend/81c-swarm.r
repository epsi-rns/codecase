# Load required libraries
library(readr)
library(tidyr)
library(ggplot2)

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Melt the series to long format for swarmplot
series_longer <- series %>%
  gather(key = "y", value = "value", -xs)

# Define custom colors (unused)
custom_colors <- c("red", "green", "blue")

# Define softer colors
# Light pink, Sky blue, Gold
soft_colors <- c("#FFB6C1", "#87CEEB", "#FFD700")

# Create swarmplot using ggplot2 with custom colors
plot <- ggplot(
    series_longer,
    aes(x = y, y = value, color = y)) +
  geom_point(
    position = position_jitterdodge(
      jitter.width = 0.3, jitter.height = 0),
    size = 0.5) +
  scale_fill_manual(values = soft_colors) +
  labs(
    x = "Variable", y = "Value",
    title = "Swarm Plot for ys1, ys2, and ys3") +
  theme_minimal() +
  theme(
    text = element_text(size = 4))

# Save plot as PNG
ggsave("81c-swarm.png", plot,
  width = 800, height = 400, units = "px")
