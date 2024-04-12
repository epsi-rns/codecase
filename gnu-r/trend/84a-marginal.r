# Load required libraries
library(readr)
library(ggplot2)
library(ggExtra)

# Avoid generating Rplots.pdf
pdf(NULL)

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Create scatter plot with marginal density plots
p <- ggplot(
    series, linewidth = 0.2,
    aes(x = xs, y = ys3)) +
  geom_point(size = 0.2) +
  geom_smooth(
    method = "lm", formula = y ~ poly(x, 1),
    se = TRUE, color = "blue", linewidth = 0.2) +
  theme_minimal() +
  theme(
    text = element_text(size = 4))

# Add marginal density plots
p_with_margins <- ggMarginal(
  p, type = "density", linewidth = 0.2,)

# Save plot as PNG
ggsave("84a-marginal.png", p_with_margins,
  width = 800, height = 600, units = "px")
