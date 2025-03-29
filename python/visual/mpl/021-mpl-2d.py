import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt

def f(x):
    return x**2 - 12*x - 64

x    = np.arange(-6, 16, 0.2)
xdot = np.arange(-6, 16, 1)

plt.plot(x, f(x), 'k', xdot, f(xdot), 'bo')
plt.axis([-10, 20, -120, 60])

plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

plt.grid()
plt.suptitle('Easy Quadratic Chart')
plt.title(r'$y = x^2 - 12x - 64$', fontsize=16, color='b', y=1.04)
plt.xlabel('Just X')
plt.ylabel('Just Y')

plt.show()
