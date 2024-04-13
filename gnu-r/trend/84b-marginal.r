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

# Create scatter plot with marginal histogram plots
p <- ggplot(
    series, linewidth = 0.2,
    aes(x = xs, y = ys3)) +
  geom_point(size = 0.2) +
  geom_smooth(
    method = "lm", formula = y ~ poly(x, 1),
    color = "red", fill = alpha("#87CEEB", 0.1),
    se = TRUE, linewidth = 0.2) +
  theme_minimal() +
  theme(
    text = element_text(size = 4))

# Add marginal histogram plots
p_with_margins <- ggMarginal(
  p, type = "histogram",
  color = "black", fill = alpha("#FFD700", 0.1),
  linewidth = 0.1)

# Save plot as PNG
ggsave("84b-marginal.png", p_with_margins,
  width = 800, height = 600, units = "px")
