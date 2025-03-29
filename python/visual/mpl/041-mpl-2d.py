import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class QuadraticAnimator:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.x = np.linspace(-10, 20, 400)

        # Set up the plot
        self.ax.set_xlim(-10, 20)
        self.ax.set_ylim(-150, 100)
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')
        self.ax.grid()
        self.ax.set_xlabel("X-Axis")
        self.ax.set_ylabel("Y-Axis")

        # Static equation text
        self.eq_text = self.ax.text(
            0.05, 0.9, r"$y = ax^2 + bx + c$",
            transform=self.ax.transAxes, fontsize=16, color='b')

        # Dynamic coefficient text
        self.coeff_text = self.ax.text(
            0.05, 0.8, "", transform=self.ax.transAxes,
            fontsize=14, color='r')

        # Line and points
        self.line, = self.ax.plot([], [], 'k')
        self.points, = self.ax.plot([], [], 'bo')

        # Animation settings

        # Frames per scene
        self.scene_duration = 60

        # Frames to pause before next scene
        self.pause_duration = 20

        # Full cycle
        self.total_frames = 3 * (
            self.scene_duration + self.pause_duration)

    def quadratic_function(self, x, a, b, c):
        # Compute y values for the quadratic function.
        return a * x**2 + b * x + c

    def update(self, frame):
        # Update function for animation.

        # Determine scene index
        scene = frame // (
            self.scene_duration + self.pause_duration)

        # Frame within the scene
        scene_frame = frame % (
            self.scene_duration + self.pause_duration)

        # Pause before switching to the next scene
        if scene_frame >= self.scene_duration:
            return self.line, self.points, self.coeff_text

        # Normalize time within the scene
        t = scene_frame / self.scene_duration

        # Moves from +1 to -1 to +1 smoothly
        direction = np.cos(t * np.pi * 2)

        if scene == 0:  # Change a only
            # Varies from +2 to -2 and back
            a = 2 * direction
            b, c = - 12, -64
        elif scene == 1:  # Change b only
            a, c = 1, -64
            # Varies from -12 to +12 and back
            b = - 12 * direction
        else:  # Change c only
            a, b = 1, -12
            # Varies from -64 to +64 and back
            c = -64 * direction

        y = self.quadratic_function(self.x, a, b, c)
        self.line.set_data(self.x, y)

        xdot = np.arange(-6, 16, 1)
        ydot = self.quadratic_function(xdot, a, b, c)
        self.points.set_data(xdot, ydot)

        # Update dynamic text
        self.coeff_text.set_text(
            r"$a = {:.1f}, b = {:.1f}, c = {:.1f}$"\
                .format(a, b, c))

        return self.line, self.points, self.coeff_text

    def animate(self):
        """Run the animation."""
        ani = animation.FuncAnimation(
            self.fig, self.update,
            frames=self.total_frames,
            interval=100, blit=False, repeat=True)
        plt.show()


    def save_animation(self,
            filename="quadratic-animation-mpl.mp4", fps=30):
        # Save the animation as a video.
        ani = animation.FuncAnimation(
            self.fig, self.update, frames=self.total_frames,
            interval=100, blit=False, repeat=True)

        writer = animation.FFMpegWriter(fps=fps)
        ani.save(filename, writer=writer)
        print(f"Animation saved as {filename}")

# Run animation
if __name__ == "__main__":
    animator = QuadraticAnimator()
    animator.save_animation()
    animator.animate()
