import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class QuadraticSurfaceAnimator:
    def __init__(self):
        sns.set_style("whitegrid")
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(
            111, projection='3d')

        # Define grid
        self.X = np.arange(-5, 5.1, 0.2)
        self.Y = np.arange(-5, 5.1, 0.2)
        self.X, self.Y = np.meshgrid(self.X, self.Y)

        # Seaborn color palette
        self.colors = sns.color_palette("dark", 6)
        self.cmap = sns.color_palette(
            "coolwarm", as_cmap=True)

        # Animation settings
        self.scene_duration = 60
        self.pause_duration = 20
        self.total_frames = 6 * (
            self.scene_duration + self.pause_duration)

        # Plot settings
        self.ax.set_zlim(-151, 76)
        self.ax.set_xlabel("X-Axis")
        self.ax.set_ylabel("Y-Axis")
        self.ax.set_zlabel("Z-Axis")

        # Static equation text
        self.eq_text = self.ax.text2D(
            0.1, 0.9, r"$z = ax^2 + by^2 + cx + dy + exy + f$",
            transform=self.fig.transFigure,
            fontsize=14, color=self.colors[0])

        # Dynamic coefficient text
        self.coeff_text = self.ax.text2D(
            0.1, 0.85, "",
            transform=self.fig.transFigure,
            fontsize=12, color=self.colors[2])

        # Initial plot
        self.surf = None

    def quadratic_surface(self, x, y, a, b, c, d, e, f):
        return a * x**2 + b * y**2 + c * x + d * y + e * x * y + f

    def update(self, frame):
        scene = frame // (
            self.scene_duration + self.pause_duration)
        scene_frame = frame % (
            self.scene_duration + self.pause_duration)

        if scene_frame >= self.scene_duration:
            return self.surf, self.coeff_text

        t = scene_frame / self.scene_duration
        direction = np.cos(t * np.pi * 2)

        # Default values
        a, b, c, d, e, f = 1, 1, -12, 12, 1, -64

        if scene == 0:
            a = 2 * direction  # Change a
        elif scene == 1:
            b = 2 * direction  # Change b
        elif scene == 2:
            c = -12 * direction  # Change c
        elif scene == 3:
            d = 12 * direction  # Change d
        elif scene == 4:
            e = 1 * direction  # Change e
        else:
            f = -64 * direction  # Change f

        Z = self.quadratic_surface(self.X, self.Y, a, b, c, d, e, f)

        if self.surf:
            self.surf.remove()

        self.surf = self.ax.plot_surface(
            self.X, self.Y, Z, cmap=self.cmap,
            linewidth=0, antialiased=True)
        self.coeff_text.set_text(
            r"$a={:.1f}, b={:.1f}, c={:.1f}, d={:.1f}, e={:.1f}, f={:.1f}$"\
                .format(a, b, c, d, e, f))

        return self.surf, self.coeff_text

    def animate(self):
        ani = animation.FuncAnimation(
            self.fig, self.update,
            frames=self.total_frames, interval=100, blit=False, repeat=True)
        plt.show()

    def save_animation(self,
            filename="quadratic-surface-sb.mp4", fps=30):

        # Save the animation as a video.
        ani = animation.FuncAnimation(
            self.fig, self.update,
            frames=self.total_frames, interval=100, blit=False, repeat=True)
        writer = animation.FFMpegWriter(fps=fps)
        ani.save(filename, writer=writer)
        print(f"Animation saved as {filename}")

# Run animation
if __name__ == "__main__":
    animator = QuadraticSurfaceAnimator()
    animator.save_animation()
    animator.animate()
