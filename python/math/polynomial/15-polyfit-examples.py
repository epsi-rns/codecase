import numpy as np
import matplotlib.pyplot as plt

from typing import List

class CurveFitting:
  def __init__(self, order: int,
      xs, ys : List[int]) -> None:

    # Curve Fitting Order
    self.order = order

    # Given data
    self.xs = np.array(xs)
    self.ys = np.array(ys)

  def calc_coeff(self) -> None:
    # Perform regression using polyfit,
    mC = np.polyfit(self.xs, self.ys, deg=self.order)

    # Get coefficient matrix
    self.mCoeff = np.flip(mC)

    # Display
    coeff_text = {
      1: '(a, b)', 2: '(a, b, c)', 3: '(a, b, c, d)'}
    print('Using polyfit')
    print(f'Coefficients {coeff_text[self.order]}:'
      + f'\n\t{self.mCoeff}\n')

  def calc_plot_1st(self) -> None:
    [a, b] = self.mCoeff    
    xp = self.x_plot
    self.y_plot = a + b * xp

  def calc_plot_2nd(self) -> None:
    [a, b, c] = self.mCoeff    
    xp = self.x_plot
    self.y_plot = a + b * xp + c * xp**2

  def calc_plot_3rd(self) -> None:
    [a, b, c, d] = self.mCoeff
    xp = self.x_plot
    self.y_plot = a + b * xp + c * xp**2 + d * xp**3

  def draw_plot(self) -> None:
    label = {
      1: 'Linear Equation',
      2: 'Fitted second-order polynomial',
      3: 'Fitted third-order polynomial' }

    plt.scatter(self.xs, self.ys, label='Data points')
    plt.plot(self.x_plot, self.y_plot, color='red',
      label=label[self.order])

    suptitle = {
      1: 'Straight line fitting',
      2: 'Second-order polynomial curve fitting',
      3: 'Third-order polynomial curve fitting' }

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.suptitle(suptitle[self.order])

    subfmt = {
      1: 'a = %.2f, b = %.2f',
      2: 'a = %.2f, b = %.2f, c = %.2f',
      3: 'a = %.2f, b = %.2f, c = %.2f, d = %.2f' }

    title = subfmt[self.order] % tuple(self.mCoeff)
    plt.title(title, y=-0.01)

    plt.show()

  def process(self) -> None:
    self.calc_coeff()

    self.x_plot = np.linspace(
      min(self.xs), max(self.xs), 100)

    order_functions = {
      1: self.calc_plot_1st,
      2: self.calc_plot_2nd,
      3: self.calc_plot_3rd }
 
    if self.order in order_functions:
      order_functions[self.order]()

    self.draw_plot()

def main() -> int:
  order = 2

  xs = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  ys1 = [ 5, 9, 13, 17, 21, 25, 29,
    33, 37, 41, 45, 49, 53]
  ys2 = [ 5, 12, 25, 44, 69, 100, 137,
    180, 229, 284, 345, 412, 485]
  ys3 = [ 5, 14, 41, 98, 197, 350, 569,
    866, 1253, 1742, 2345, 3074, 3941]

  example = CurveFitting(order, xs, ys3)
  example.process()
  
  return 0

if __name__ == "__main__":
  raise SystemExit(main())

