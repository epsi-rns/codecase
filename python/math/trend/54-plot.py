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

def plot() -> None:
  plt.figure(figsize=(10, 6))

  # Plot the data series
  plt.scatter(x_observed, y_observed,
    color=blueScale[9], s=100, zorder=5,
    label='Data Points')

  # Plot deviation from mean
  plt.axhline(y=y_mean, color=blueScale[7],
    linestyle='--',  label='Mean of y')
  plt.vlines(x_observed, y_observed, y_mean,
    linestyle='--', color=blueScale[5],
    label='Deviation from Mean (y)')

  # Plot shaded region for standard deviation
  plt.fill_between(x_observed,
    y_mean - y_std_dev, y_mean + y_std_dev,
    color=blueScale[1], alpha=0.3, zorder=1,
    label='Standard Deviation')

  # Plot covariance
  plt.text(x_mean, max(y_observed),
    f'Covariance: {xy_covariance:.2f}',
    fontsize=12, color=blueScale[9])

  # Chart Decoration
  plt.title('Mean and Deviation')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend()
  plt.grid(True)

  plt.show()

  return 0

if __name__ == "__main__":
  raise SystemExit(plot())