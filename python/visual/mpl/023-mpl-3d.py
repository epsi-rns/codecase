import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import (
    LinearLocator, FormatStrFormatter)

class QuadraticSurfacePlot:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(
          111, projection='3d')

    def f(self, x, y):
        return x**2 + y**2 - 12*x + 12*y + x*y - 64

    def generate_data(self):
        X = np.arange(-5, 5.1, 0.2)
        Y = np.arange(-5, 5.1, 0.2)
        self.X, self.Y = np.meshgrid(X, Y)
        self.Z = self.f(self.X, self.Y)

        Xline = np.arange(-5, 5.1, 1)
        Yline = np.arange(-5, 5.1, 1)
        self.Xline, self.Yline = np.meshgrid(Xline, Yline)
        self.Zline = self.f(self.Xline, self.Yline)

    def plot_surface(self):
        self.surf = self.ax.plot_surface(
            self.X, self.Y, self.Z, cmap=cm.viridis,
            linewidth=1, antialiased=False)
        self.wire = self.ax.plot_wireframe(
            self.Xline, self.Yline, self.Zline)

    def customize_axes(self):
        self.ax.set_zlim(-151, 76)
        self.ax.zaxis.set_major_locator(
            LinearLocator(10))
        self.ax.zaxis.set_major_formatter(
            FormatStrFormatter('%.02f'))

    def add_colorbar(self):
        self.fig.colorbar(
            self.surf, shrink=0.5, aspect=5)

    def add_quiver(self):
        x, y, z = np.zeros((3, 3))
        u, v, w = np.array(
            [[1, 1, 0], [1, 0, 1], [0, 1, 1]])
        self.ax.quiver(
            x, y, z, u, v, w, arrow_length_ratio=0.1)

    def decorate_plot(self):
        plt.suptitle('Easy Quadratic Chart')
        plt.xlabel('Just X')
        plt.ylabel('Just Y')
        self.ax.set_zlabel('Just Z', rotation=90)
        self.ax.set_zticks(np.arange(-150, 50, 25))
        plt.title(
            r'$z = x^2 + y^2 - 12x + 12y + xy - 64$',
            fontsize=16, color='b', y=1.06)

    def show(self):
        plt.show()

    def plot(self):
        self.generate_data()
        self.plot_surface()
        self.customize_axes()
        self.add_colorbar()
        self.add_quiver()
        self.decorate_plot()
        self.show()

# Run the plot
if __name__ == "__main__":
    plotter = QuadraticSurfacePlot()
    plotter.plot()
