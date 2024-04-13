# Load required libraries
library(readr)
library(ggplot2)
library(ggthemes)

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

# Scatter plot with regression lines
plot <- ggplot(data, aes(x = xs)) +
  # Add points for y1,
  # add regression line for y1
  geom_point(
    aes(x = xs, y = ys1),
    size = 0.5, color = "firebrick") +  
  geom_smooth(
    aes(x = xs, y = ys1), method = "lm",
    se = TRUE, color = "firebrick",
    linewidth = 0.2) +  

  # Add points for y2,
  # add quadratic regression line for y2
  geom_point(
    aes(x = xs, y = ys2),
    size = 0.5, color = "forestgreen") +  
  geom_smooth(
    aes(x = xs, y = ys2), method = "lm",
    # formula = y ~ poly(x, 2),
    se = TRUE, color = "forestgreen",
    linewidth = 0.2) +  

  # Add points for y3,
  # add cubic regression line for y3
  geom_point(
    aes(x = xs, y = ys3),
    size = 0.5, color = "royalblue") +  
  geom_smooth(
    aes(x = xs, y = ys3), method = "lm",
    # formula = y ~ poly(x, 3),
    se = TRUE, color = "royalblue",
    linewidth = 0.2) +  

  labs(x = "x", y = "y",
    title = "Scatter Plot with Regression Lines") +
  theme_solarized() +
  scale_color_solarized() +
  theme(
    text = element_text(size = 4))

# Save plot as PNG
ggsave("71-geom-smooth.png", plot,
  width = 800, height = 400, units = "px")
