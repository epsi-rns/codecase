import numpy as np
from scipy.stats import linregress
from typing import Dict

class Dict2Obj:
    def __init__(self, properties_dict):
        self.__dict__.update(properties_dict)

def get_properties(file_path) -> Dict:
  # Getting Matrix Values
  pairCSV = np.genfromtxt(file_path,
    skip_header=1, delimiter=",", dtype=float)
  
  # Extract x and y values from CSV data
  x_observed = pairCSV[:, 0]
  y_observed = pairCSV[:, 1]

  # Number of data points
  n = len(x_observed)

  # Calculate sums
  x_sum = np.sum(x_observed)
  y_sum = np.sum(y_observed)

  # Calculate means
  x_mean = np.mean(x_observed)
  y_mean = np.mean(y_observed)

  # Calculate variance
  x_variance = np.var(x_observed)
  y_variance = np.var(y_observed)

  # Calculate covariance
  xy_covariance = np.cov(x_observed, y_observed)[0, 1]

  # Calculate standard deviations
  x_std_dev = np.std(x_observed)
  y_std_dev = np.std(y_observed)

  # Calculate slope (m), intercept (b),
  # and other regression parameters
  m_slope, b_intercept, r_value, p_value, \
  std_err_slope = linregress(x_observed, y_observed)

  # Create regression line
  y_fit = m_slope * x_observed + b_intercept
  y_err = y_observed - y_fit

  return locals()

def display(properties: Dict) -> None:
  p = Dict2Obj(properties)

  # Output basic properties
  print(f'{f"n":10s} = {p.n:4d}')
  print(f'∑x (total) = {p.x_sum:7.2f}')
  print(f'∑y (total) = {p.y_sum:7.2f}')
  print(f'x̄ (mean)   = {p.x_mean:7.2f}')
  print(f'ȳ (mean)   = {p.y_mean:7.2f}')
  print()

  # Output statistics properties
  print(f'sₓ² (variance) = {p.x_variance:9.2f}')
  print(f'sy² (variance) = {p.y_variance:9.2f}')
  print(f'covariance     = {p.xy_covariance:9.2f}')
  print(f'sₓ (std dev)   = {p.x_std_dev:9.2f}')
  print(f'sy (std dev)   = {p.y_std_dev:9.2f}')
  print(f'm (slope)      = {p.m_slope:9.2f}')
  print(f'b (intercept)  = {p.b_intercept:9.2f}')
  print()

  print(f'Equation     y = ' \
    + f'{p.b_intercept:5.2f} + {p.m_slope:5.2f}.x')
  print()
