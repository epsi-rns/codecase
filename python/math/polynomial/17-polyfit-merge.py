import numpy as np
import matplotlib.pyplot as plt

from typing import List

class CurveFitting:
  def __init__(self, xs, ys : List[int]) -> None:

    # Given data
    self.xs = np.array(xs)
    self.ys = np.array(ys)

  def calc_coeff(self, order) -> np.ndarray:
    # Perform regression using polyfit,
    mC = np.polyfit(self.xs, self.ys, deg=order)

    # Display
    coeff_text = {
      1: '(a, b)', 2: '(a, b, c)', 3: '(a, b, c, d)'}

    print('Using polyfit')
    print(f'Coefficients {coeff_text[order]}:'
      + f'\n\t{np.flip(mC)}\n')

    # Get coefficient matrix
    return np.flip(mC)

  def calc_plot_all(self) -> None:
    self.x_plot = xp = np.linspace(
      min(self.xs), max(self.xs), 100)

    [a1, b1] = self.mCoeff_1st
    self.y1_plot = a1 + b1 * xp

    [a2, b2, c2] = self.mCoeff_2nd
    self.y2_plot = a2 + b2 * xp + c2 * xp**2

    [a3, b3, c3, d3] = self.mCoeff_3rd
    self.y3_plot = a3 + b3 * xp + c3 * xp**2 + d3 * xp**3

  def draw_plot(self) -> None:
    label = {
      1: 'Linear Equation',
      2: 'Fitted second-order polynomial',
      3: 'Fitted third-order polynomial' }

    plt.scatter(self.xs, self.ys, label='Data points', color='teal')
    plt.plot(self.x_plot, self.y1_plot, color='red',
      label='Linear Equation')
    plt.plot(self.x_plot, self.y2_plot, color='green',
      label='Fitted second-order polynomial')
    plt.plot(self.x_plot, self.y3_plot, color='blue',
      label='Fitted third-order polynomial')

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.suptitle('suptitle')

    plt.title('equation', y=-0.01)

    plt.show()

  def process(self) -> None:
    self.mCoeff_1st = self.calc_coeff(1)
    self.mCoeff_2nd = self.calc_coeff(2)
    self.mCoeff_3rd = self.calc_coeff(3)

    self.calc_plot_all()



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

  example = CurveFitting(xs, ys3)
  example.process()
  
  return 0

if __name__ == "__main__":
  raise SystemExit(main())

