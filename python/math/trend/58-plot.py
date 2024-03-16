import matplotlib.pyplot as plt

# Local Library
from Properties import get_properties, display

# Load properties from Properties.py helper
# and unpack them into local variables
properties = get_properties("50-samples.csv")
display(properties)
locals().update(properties)

tealScale = {
  0: '#E0F2F1', 1: '#B2DFDB', 2: '#80CBC4',
  3: '#4DB6AC', 4: '#26A69A', 5: '#009688',
  6: '#00897B', 7: '#00796B', 8: '#00695C',
  9: '#004D40'
}

def plot() -> None:
  plt.figure(figsize=(10, 6))

  # Plot the data and regression line
  plt.scatter(x_observed, y_observed,
    color=tealScale[9], label='Data Points')
  plt.plot(x_observed, y_fit,
    color=tealScale[5], label='Regression Line')

  plt.plot(x_observed, y_fit + y_std_dev,
    c=tealScale[1], linestyle='--')
  plt.plot(x_observed, y_fit - y_std_dev,
    c=tealScale[1], linestyle='--',
    label='Regression ± Standard Deviation')

  # Fill between upper and lower bounds
  plt.fill_between(x_observed,
  y_fit - y_std_dev, y_fit + y_std_dev,
  color=tealScale[1], alpha=0.3,
  label='Standard Deviation')

  # Chart Decoration
  plt.title('Standard Deviation')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend()
  plt.grid(True)

  plt.show()

  return 0

if __name__ == "__main__":
  raise SystemExit(plot())
