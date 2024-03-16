import matplotlib.pyplot as plt

# Local Library
from Properties import get_properties, display

# Load properties from Properties.py helper
# and unpack them into local variables
properties = get_properties("50-samples.csv")
display(properties)
locals().update(properties)


def plot() -> None:
  plt.figure(figsize=(10, 6))

  # Plot the data and the mean as axis
  plt.scatter(x_observed, y_observed,
    color='blue', label='Data Points')

  plt.axvline(x=x_mean, color='green',
    linestyle='--', label='Mean of x')
  plt.axhline(y=y_mean, color='orange',
    linestyle='--', label='Mean of y')

  # Plot standard deviation as error bars
  plt.errorbar(x_mean, y_mean,
    xerr=x_std_dev, yerr=y_std_dev,
    fmt='o', color='purple', label='Standard Deviation')

  # Chart Decoration
  plt.title('Linear Regression')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend()
  plt.grid(True)

  plt.show()

  return 0

if __name__ == "__main__":
  raise SystemExit(plot())