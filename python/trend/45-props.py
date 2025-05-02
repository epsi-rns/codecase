import numpy as np
from numpy.polynomial import Polynomial
from scipy.stats import t
from sklearn.metrics import r2_score
from typing import List

class PolynomialOrderAnalyzer:
    def __init__(self, xs, ys: np.ndarray, order: int) -> None:
        self.xs = xs
        self.ys = ys
        self.order = order
        self.df = len(self.xs) - order -1

        self.mA   = None
        self.mC   = None
        self.yp   = None
        self.diag = None
        self.MSE  = None

        # Display
        coeff_text_s = {
            1: '(a, b)', 2: '(a, b, c)', 3: '(a, b, c, d)'}
        order_text_s = {
            1: 'Linear',  2: 'Quadratic ', 3: 'Cubic'}
        self.coeff_text = coeff_text_s[order]
        self.order_text = order_text_s[order]
       
    def calc_props_matrix(self) -> None:
        # Perform regression     
        # mA_1 = np.column_stack([np.ones_like(self.xs), self.xs, self.xs**2])
        # mA_2 = np.column_stack([self.xs**j for j in range(self.order+1)])  # Design matrix
        self.mA = np.flip(np.vander(self.xs, self.order+1), axis=1)

        # matrix operation
        mB = self.ys
        mAt   = self.mA.T
        mAt_A = mAt @ self.mA # gram matrix
        mAt_B = mAt @ mB 
        # mC_1 = np.linalg.solve(mAt_A, mAt_B)
        # mC_2 = np.polyfit(self.xs, self.ys, deg=order)
        # mC_3 = np.linalg.inv(self.mA.T @ self.mA) @ (self.mA.T @ mB)
        # mC_4 = np.linalg.lstsq(self.mA, mB, rcond=None)[0]
        # print(mC_4)
        mI   = np.linalg.inv(mAt_A)
        self.diag = np.diag(mI)

        # Perform regression using polyfit,
        poly = Polynomial.fit(self.xs, self.ys, deg=self.order)
        self.mC = poly.convert().coef
        # yp_1    = np.polyval(mC, self.xs)
        self.yp = poly(self.xs)
        # y_pred_2 = self.mA @ mC
        # print(y_pred_2)

        print(f'Using polyfit : {self.order_text}')
        print(f'Coefficients  : {self.coeff_text}: '
            + f'{self.mC}')

    def calc_props_mse(self) -> None:
        # Calculate SST and SSE
        y_mean = np.mean(self.ys)
        SST = y_sq_deviation = np.sum((self.ys-y_mean) ** 2)
        SSR = np.sum((self.ys - self.yp) ** 2) # ∑ϵᵢ²
        R_squared = 1 - (SSR / SST)
        self.MSE = SSR/self.df

        print(f'\t∑(yᵢ - ŷᵢ)² : {SSR:15,.2f}')
        print(f'\tR²          : {R_squared:15,.4f}')
        print(f'\tMSE         : {self.MSE:15,.2f}')

    def calc_props_t_p_value(self) -> None:
        # t-value, p-value
        SE   = np.sqrt(self.MSE * self.diag)
        t_value = self.mC/SE
        p_value = 2 * (1 - t.cdf(abs(t_value), self.df))

        diag_formatted = [f"{x:15,.4f}" for x in self.diag]
        SE_formatted   = [f"{x:15,.4f}" for x in SE]
        t_v_formatted  = [f"{x:15,.2e}" for x in t_value]
        p_v_formatted  = [f"{x:15,.10f}" for x in p_value]
        
        print(f"diag    : [" + " ".join(diag_formatted) + "]")
        print(f"SE(β)   : [" + " ".join(SE_formatted) + "]")
        print(f"t_value : [" + " ".join(t_v_formatted) + "]")
        print(f"p_value : [" + " ".join(p_v_formatted) + "]")

        print()

class CurveFitting:
    def __init__(self, xs, ys : List[int]) -> None:
        # Given data
        self.xs = np.array(xs)
        self.ys = np.array(ys)

    def print_props_general(self) -> None:
        y_mean = np.mean(self.ys)
        self.y_sq_deviation = np.sum((self.ys-y_mean) ** 2)
        print('General')
        print(f'\tȳ (mean)   : {y_mean:15,.2f}')
        print(f'\t∑(yᵢ-ȳ)²   : {self.y_sq_deviation:15,.2f}')
        print()

    def process(self) -> None:
        # Print Statistical Properties
        self.print_props_general()
        
        for order in [1, 2, 3]:
            case = PolynomialOrderAnalyzer(self.xs, self.ys, order)
            case.calc_props_matrix()
            case.calc_props_mse()
            case.calc_props_t_p_value()

def main() -> int:
    # Getting Matrix Values
    mCSV = np.genfromtxt("series.csv",
      skip_header=1, delimiter=",", dtype=float)
    mCSVt   = np.transpose(mCSV)

    example = CurveFitting(mCSVt[0], mCSVt[3])
    example.process()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

