# Load required libraries
library(readr)
library(ggplot2)
library(ggthemes)
library(gridExtra)

# Avoid generating Rplots.pdf
pdf(NULL)

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Extract x and y values from CSV data
xs <- series$xs
ys1 <- series$ys1
ys2 <- series$ys2
ys3 <- series$ys3

# Create a data frame with x and y values
data <- data.frame(
  x = xs, y1 = ys1, y2 = ys2, y3 = ys3)

# Scatter plot with regression line for y1
plot_y1 <- ggplot(data, aes(x = xs, y = ys1)) +
  geom_point(
    size = 0.5, color = "indianred") +  
  geom_smooth(
    method = "lm", formula = y ~ poly(x, 1),
    se = TRUE, color = "indianred", linewidth = 0.2) +  
  labs(
    x = "x", y = "y", 
    title = "Regression Line for y1") +
  theme_light() +
  theme(
    text = element_text(size = 2),
    axis.text = element_text(size = 3))

# Scatter plot with quadratic regression line for y2
plot_y2 <- ggplot(data, aes(x = xs, y = ys2)) +
  geom_point(
    size = 0.5, color = "limegreen") +  
  geom_smooth(
    method = "lm", formula = y ~ poly(x, 1),
    se = TRUE, color = "limegreen", linewidth = 0.2) +  
  labs(
    x = "x", y = "y", 
    title = "Quadratic Regression Line for y2") +
  theme_light() +
  theme(
    text = element_text(size = 2),
    axis.text = element_text(size = 3))

# Scatter plot with cubic regression line for y3
plot_y3 <- ggplot(data, aes(x = xs, y = ys3)) +
  geom_point(
    size = 0.5, color = "steelblue") +  
  geom_smooth(
    method = "lm", formula = y ~ poly(x, 1),
    se = TRUE, color = "steelblue", linewidth = 0.2) +  
  labs(
    x = "x", y = "y", 
    title = "Cubic Regression Line for y3") +
  theme_light() +
  theme(
    text = element_text(size = 2),
    axis.text = element_text(size = 3))

# Arrange plots using gridExtra horizontally
grid_plot <- grid.arrange(
  plot_y1, plot_y2, plot_y3, ncol = 3)

# Save the combined grid of plots as PNG
ggsave("72-grid-extra.png", grid_plot,
  width = 800, height = 400, units = "px")
