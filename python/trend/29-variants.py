import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import (
    Polynomial, Chebyshev, Legendre, Hermite)

# Create x values
x = np.linspace(-1.1, 1.1, 400)

# Degree 3 polynomials with simple coefficients for comparison
coeffs = [5, 4, 3, 2]

# Generate polynomial curves
y_poly = Polynomial(coeffs)(x)
y_cheb = Chebyshev(coeffs)(x)
y_legendre = Legendre(coeffs)(x)
y_hermite = Hermite(coeffs)(x)

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(x, y_poly, label="Regular Polynomial", linewidth=2)
plt.plot(x, y_cheb, label="Chebyshev Series", linestyle='--')
plt.plot(x, y_legendre, label="Legendre Series", linestyle='-.')
plt.plot(x, y_hermite, label="Hermite Series", linestyle=':')

plt.title("Comparison of Polynomial Series (Degree 3)")
plt.xlabel("x")
plt.ylabel("y")

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
