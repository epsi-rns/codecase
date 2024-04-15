# Load required libraries
library(readr)
library(tidyr)
library(ggplot2)

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Melt the series to long format for violinplot
series_longer <- series %>%
  gather(key = "y", value = "value", -xs)

# Define custom colors (unused)
custom_colors <- c("red", "green", "blue")

# Define softer colors
# Light pink, Sky blue, Gold
soft_colors <- c("#FFB6C1", "#87CEEB", "#FFD700")

# Create violinplot using ggplot2 with custom colors
plot <- ggplot(
    series_longer,
    aes(x = y, y = value, fill = y)) +
  geom_violin(color = "black", linewidth= 0.2) +
  scale_fill_manual(values = soft_colors) +
  labs(
    x = "Variable", y = "Value",
    title = "Violin Plot for ys1, ys2, and ys3") +
  theme_minimal() +
  theme(
    plot.background = element_rect(fill = "white"),
    text = element_text(size = 4))

# Save plot as PNG
ggsave("81b-violin.png", plot,
  width = 800, height = 400, units = "px")
