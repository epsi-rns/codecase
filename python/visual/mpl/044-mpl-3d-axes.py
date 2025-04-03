import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.ticker import (LinearLocator, FormatStrFormatter)
from matplotlib.animation import FuncAnimation

matplotlib.rcParams['text.usetex'] = True

class QuadraticSurfaceAnimation:
    def __init__(self):
        # Seaborn color palette
        sns.set_style("whitegrid")
        self.colors = sns.color_palette("dark", 6)
        self.cmap   = sns.color_palette(
            "Spectral", as_cmap=True)

        # Create figure and 3D axis
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(
            111, projection='3d')

        # Set initial view
        self.ax.view_init(elev=20, azim=30)

        # Set axis limits before generating data
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-151, 76)

        # Generate data and plot surface once
        self.generate_data()
        self.plot_surface()
        self.customize_axes()
        self.add_colorbar()
        self.add_quiver()
        self.decorate_plot()

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
        # Plot surface once (not updated during animation)
        self.surf = self.ax.plot_surface(
            self.X, self.Y, self.Z,
            cmap=self.cmap, linewidth=0, antialiased=False)

    def customize_axes(self):
        self.ax.zaxis.set_major_locator(
            LinearLocator(10))
        self.ax.zaxis.set_major_formatter(
            FormatStrFormatter('%.02f'))

    def add_colorbar(self):
        self.fig.colorbar(self.surf, shrink=0.5, aspect=5)

    def add_quiver(self):
        x, y, z = np.zeros((3, 3))
        # Standard basis vectors
        u, v, w = np.array(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        self.ax.quiver(
            x, y, z, u, v, w,
            arrow_length_ratio=0.1, color=['r', 'g', 'b'])

    def decorate_plot(self):
        plt.suptitle('Easy Quadratic Chart')
        plt.xlabel('Just X')
        plt.ylabel('Just Y')

        self.ax.set_zlabel('Just Z', rotation=90)
        self.ax.set_zticks(np.arange(-150, 50, 25))

        plt.title(
            r'$z = x^2 + y^2 - 12x + 12y + xy - 64$',
            fontsize=16, color='b', y=1.06)

    def update(self, frame):
        # Oscillate elevation within a smaller range
        angle_x = 45 * np.sin(2 * np.pi * frame / 100)

        # Oscillate azimuth within a smaller range
        angle_y = 45 * np.cos(2 * np.pi * frame / 100)

        # Update the view
        self.ax.view_init(
            elev=20 + angle_x, azim=30 + angle_y)

        # Return the modified artist(s)
        return self.ax,

    def animate(self):
        ani = FuncAnimation(
            self.fig, self.update,
            frames=1000, interval=1000/30,
            blit=False, repeat=True)
        plt.show()

    def save_animation(self,
            filename='quadratic-surface-view.mp4',
            fps=30, frames=1000):

        ani = FuncAnimation(
            self.fig, self.update,
            frames=frames, interval=1000/fps, blit=False)

        ani.save(filename, writer='ffmpeg', fps=fps)
        print(f'Animation saved as {filename}')

# Run animation
if __name__ == "__main__":
    animator = QuadraticSurfaceAnimation()
    animator.save_animation()
    animator.animate()
