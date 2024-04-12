library(e1071)

# Read CSV file
pairCSV <- read.csv("50-samples.csv", header = TRUE)

# Extract x and y values from CSV data
x_observed <- pairCSV[[1]]
y_observed <- pairCSV[[2]]

# Number of data points
n <- length(x_observed)

# Calculate maximum, minimum, and range
x_max <- max(x_observed)
x_min <- min(x_observed)
x_range <- x_max - x_min

y_max <- max(y_observed)
y_min <- min(y_observed)
y_range <- y_max - y_min

# Output of maximum, minimum, and range
cat(sprintf('x (max, min, range) = (%7.2f, %7.2f, %7.2f )\n', x_min, x_max, x_range))
cat(sprintf('y (max, min, range) = (%7.2f, %7.2f, %7.2f )\n\n', y_min, y_max, y_range))

x_median <- median(x_observed)
y_median <- median(y_observed)

# Mode
x_mode <- as.numeric(names(which.max(table(x_observed))))
y_mode <- as.numeric(names(which.max(table(y_observed))))

# Output of additional properties
cat(sprintf('x median       = %9.2f\n', x_median))
cat(sprintf('y median       = %9.2f\n', y_median))
cat(sprintf('x mode         = %9.2f\n', x_mode))
cat(sprintf('y mode         = %9.2f\n\n', y_mode))

# Calculate kurtosis and skewness
x_kurtosis <- kurtosis(x_observed)
y_kurtosis <- kurtosis(y_observed)

x_skewness <- skewness(x_observed)
y_skewness <- skewness(y_observed)

cat(sprintf('x kurtosis     = %9.2f\n', x_kurtosis))
cat(sprintf('y kurtosis     = %9.2f\n', y_kurtosis))
cat(sprintf('x skewness     = %9.2f\n', x_skewness))
cat(sprintf('y skewness     = %9.2f\n\n', y_skewness))

# Number of data points
x_n <- length(x_observed)
y_n <- length(y_observed)

# Calculate SE kurtosis and SE skewness
calc_se_kurtosis_gaussian <- function(n) {
  sqrt(4 * n^2 * calc_se_skewness(n)^2 / ((n - 3) * (n + 5)))
}

calc_se_skewness <- function(n) {
  sqrt((6 * n * (n - 1)) / ((n - 2) * (n + 1) * (n + 3)))
}

x_se_kurtosis <- calc_se_kurtosis_gaussian(x_n)
y_se_kurtosis <- calc_se_kurtosis_gaussian(y_n)
x_se_skewness <- calc_se_skewness(x_n)
y_se_skewness <- calc_se_skewness(y_n)

cat(sprintf('x SE kurtosis  = %9.2f\n', x_se_kurtosis))
cat(sprintf('y SE kurtosis  = %9.2f\n', y_se_kurtosis))
cat(sprintf('x SE skewness  = %9.2f\n', x_se_skewness))
cat(sprintf('y SE skewness  = %9.2f\n', y_se_skewness))
