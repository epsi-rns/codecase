# Load required libraries
library(readr)
library(ggplot2)
library(R6)

CurveFitting <- R6Class("CurveFitting",

  public = list(
    xs  = NULL, ys  = NULL,
    lm1 = NULL, lm2 = NULL, lm3 = NULL,
    xp  = NULL, yp1 = NULL, yp2 = NULL, yp3 = NULL,

    initialize = function(xs, ys) {
      self$xs <- xs
      self$ys <- ys
    },

    generate_regressions = function() {
      # Keep the variable name for data frame
      x_values <- self$xs
    
      # Independent x values.
      self$xp <- seq(
        min(x_values), max(x_values),
        length.out = 100)

      # Generate values for the linear regression
      self$lm1 <- lm(self$ys ~
        poly(x_values, 1, raw = TRUE))
      self$yp1 <- predict(self$lm1,
        newdata = data.frame(x_values = self$xp))

      # Generate values for the quadratic regression
      self$lm2 <- lm(self$ys ~
        poly(x_values, 2, raw = TRUE))
      self$yp2 <- predict(self$lm2,
        newdata = data.frame(x_values = self$xp))

      # Generate values for the cubic regression
      self$lm3 <- lm(self$ys ~
        poly(x_values, 3, raw = TRUE))
      self$yp3 <- predict(self$lm3,
        newdata = data.frame(x_values = self$xp))
    },

    show_coeff = function(order, lm_model) {
      # Define a named vector
      # to map order numbers to curve types
      coeff_text <- c(
        "(a, b)" = 1, "(a, b, c)" = 2,
        "(a, b, c, d)" = 3)
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
    },

    show_coeffs = function() {
      self$show_coeff(1, self$lm1)
      self$show_coeff(2, self$lm2)
      self$show_coeff(3, self$lm3)
    },

    create_plot = function() {
      # Create data frame for ggplot2
      data <- data.frame(x = self$xs, y = self$ys)

      # Plot using ggplot2
      plot <- ggplot(data,
          aes(x = x, y = y, color = "Data Points")) +
        geom_point(size = 0.5) +
        geom_line(
          data = data.frame(x = self$xp, y = self$yp1),
          aes(x = x, y = y, color = "Linear Equation"),
          linewidth = 0.2) +
        geom_line(
          data = data.frame(x = self$xp, y = self$yp2),
          aes(x = x, y = y, color = "Quadratic Curve"),
          linewidth = 0.2) +
        geom_line(
          data = data.frame(x = self$xp, y = self$yp3),
          aes(x = x, y = y, color = "Cubic Curve"),
          linewidth = 0.2) +
        labs(
          x = "x", y = "y",
          title = "Polynomial Curve Fitting") +
        theme_minimal() +
        theme(
          legend.position = "right",
          legend.text = element_text(size = 2),
          plot.background = element_rect(fill = "white"),
          text = element_text(size = 4)
        ) +
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
            "Cubic Curve" = "blue"))

      # Save plot as PNG
      ggsave("19-lm-merge.png", plot,
        width = 800, height = 400, units = "px")
    }
  )
)

# Read data from CSV file
series <- read_csv(
  "series.csv",
  show_col_types = FALSE)

# Create CurveFitting object
# Perform linear regression, display, and plot
curve_fitting <- CurveFitting$new(
  series$xs, series$ys3)
curve_fitting$generate_regressions()
curve_fitting$show_coeffs()
curve_fitting$create_plot()

