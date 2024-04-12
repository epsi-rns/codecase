# Load required libraries
library(readr)
library(ggplot2)

generate_regressions <- function(x_values, y_values) {
  # Independent x values.
  x_plot <- seq(
    min(x_values), max(x_values),
    length.out = 100)

  print(length(x_values))
  print(length(x_plot))

  # Generate values for the linear regression
  lm_model_1 <- lm(y_values ~ 
    poly(x_values, 1, raw = TRUE))
  y_plot_1 <- predict(
    lm_model_1,
    newdata = data.frame(x_values = x_plot))

  # Generate values for the quadratic regression
  lm_model_2 <- lm(y_values ~ 
    poly(x_values, 2, raw = TRUE))
  y_plot_2 <- predict(
    lm_model_2,
    newdata = data.frame(x_values = x_plot))

  # Generate values for the cubic regression
  lm_model_3 <- lm(y_values ~ 
    poly(x_values, 3, raw = TRUE))
  y_plot_3 <- predict(
    lm_model_3,
    newdata = data.frame(x_values = x_plot))

  # Return a list containing all relevant objects
  return(list(
    x_values = x_values,
    y_values = y_values,
    lm_model_1 = lm_model_1,
    lm_model_2 = lm_model_2,
    lm_model_3 = lm_model_3,
    x_plot   = x_plot,
    y_plot_1 = y_plot_1,
    y_plot_2 = y_plot_2,
    y_plot_3 = y_plot_3
  ))
}

show_coeff <- function(order, lm_model) {
  # Define a named vector
  # to map order numbers to curve types
  coeff_text <- c(
    "(a, b)" = 1, "(a, b, c)" = 2, "(a, b, c, d)" = 3)
  order_text <- c(
    "Linear" = 1, "Quadratic" = 2, "Cubic" = 3)

  # Print the curve type
  cat(paste("Using lm_model :",
    names(order_text)[order], "\n"))

  # Coefficients
  coefficients <- coef(lm_model)

  # Reverse order to match output
  coefficients <- coefficients[
    length(coefficients):1]

  # Print coefficients
  cat("Coefficients ",
    names(coeff_text)[order], ":\n\t",
    coefficients, "\n")
}

create_plot <- function(regression_data) {
  x_values <- regression_data$x_values
  y_values <- regression_data$y_values
  x_plot   <- regression_data$x_plot
  y_plot_1 <- regression_data$y_plot_1
  y_plot_2 <- regression_data$y_plot_2
  y_plot_3 <- regression_data$y_plot_3

  # Create data frame for ggplot2
  data <- data.frame(x = x_values, y = y_values)

  # Plot using ggplot2
  plot <- ggplot(data, aes(x = x, y = y, color = "Data Points")) +
    geom_point(size = 0.5) +
    geom_line(
      data = data.frame(x = x_plot, y = y_plot_1),
      aes(x = x, y = y, color = "Linear Equation"),
      linewidth = 0.2) +
    geom_line(
      data = data.frame(x = x_plot, y = y_plot_2),
      aes(x = x, y = y, color = "Quadratic Curve"),
      linewidth= 0.2) +
    geom_line(
      data = data.frame(x = x_plot, y = y_plot_3),
      aes(x = x, y = y, color = "Cubic Curve"),
      linewidth = 0.2) +
    labs(
      x = "x", y = "y",
      title = "Polynomial Curve Fitting") +
    theme_minimal() +
    theme(legend.position = "right",
          legend.text = element_text(size = 2),
          text = element_text(size = 4)) +
    scale_color_manual(
      name = "Plot",
      breaks = c(
        "Data Points",
        "Linear Equation",
        "Quadratic Curve",
        "Cubic Curve"),
      values = c(
        "Data Points" = "black",
        "Linear Equation" = "red", 
        "Quadratic Curve" = "green", 
        "Cubic Curve" = "blue")) +
    guides(
      color = guide_legend(
        override.aes = list(
          shape = c(4, NA), linetype = c(0, 1)
        )))

  # Save plot as PNG
  ggsave("18-lm-merge.png", plot,
    width = 800, height = 400, units = "px")
}

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Get regression data
regress <- generate_regressions(
    series$xs, series$ys3)

# Perform linear regression and plot
show_coeff(1, regress$lm_model_1)
show_coeff(2, regress$lm_model_2)
show_coeff(3, regress$lm_model_3)
plot <- create_plot(regress)



