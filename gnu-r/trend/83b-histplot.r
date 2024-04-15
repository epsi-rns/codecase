# Load required libraries
library(readr)
library(tidyr)
library(ggplot2)

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Melt the series to long format for histplot
series_longer <- series %>%
  gather(key = "Category", value = "value", -xs)

# Create KDE plot using ggplot2 with custom colors
plot <- ggplot(
    series_longer,
    aes(x = value, fill = Category)) +
  geom_histogram(
    binwidth = 50, linewidth = 0.2,
    alpha = 0.7, color = "black") +
  scale_fill_brewer(palette = "Set1") +
  labs(
    x = "Value", y = "Density",
    title = "Histogram Plot for ys1, ys2, and ys3") +
  theme_minimal() +
  theme(
    plot.background = element_rect(fill = "white"),
    text = element_text(size = 4))

# Save plot as PNG
ggsave("83b-histplot.png", plot,
  width = 800, height = 400, units = "px")
