import matplotlib.pyplot as plt

# Local Library
from Properties import get_properties, display

# Load properties from Properties.py helper
# and unpack them into local variables
properties = get_properties("50-samples.csv")
display(properties)
locals().update(properties)

blueScale = {
  0: '#E3F2FD', 1: '#BBDEFB', 2: '#90CAF9',
  3: '#64B5F6', 4: '#42A5F5', 5: '#2196F3',
  6: '#1E88E5', 7: '#1976D2', 8: '#1565C0',
  9: '#0D47A1'
}

def plot() -> int:
  plt.figure(figsize=(10, 6))

  # Plot the data and regression line
  plt.scatter(x_observed, y_observed,
    color=blueScale[9], label='Data Points')
  plt.plot(x_observed, y_fit,
    color=blueScale[5], label='Regression Line')

  # Plot residual errors
  plt.vlines(x_observed, y_observed, y_fit,
  linestyle='--', color=blueScale[3], label='Residual')

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

