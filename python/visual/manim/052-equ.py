from manim import *

# Define colors
CONFIG = {
    "color_bg": WHITE,
    "color_fg": BLACK
}

class InverseFunction(Scene):
    def construct(self):
        self.setup_scene()
        equations = self.get_equations()
        self.animate_equations(equations)
        self.wait(2)

    def setup_scene(self):
        self.camera.background_color = CONFIG["color_bg"]

    def get_equations(self):
        return [
            MathTex(
                r"f(x) = \frac{2x}{4x - 7},"
                r" \quad x \neq \frac{7}{4}",
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\Rightarrow \quad y = \frac{2x}{4x - 7}",
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\Rightarrow \quad 4xy - 7y = 2x",
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\Rightarrow \quad 4xy - 2x = 7y",
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\Rightarrow \quad x(4y - 2) = 7y",
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\Rightarrow \quad x = \frac{7y}{4y - 2}",
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\therefore \quad f(x)^{-1} = \frac{7x}{4x - 2},"
                r"\quad x \neq \frac{1}{2}",
                color=CONFIG["color_fg"]
            ),
        ]

    def animate_equations(self, equations):
        for i, eq in enumerate(equations):
            eq.to_edge(UP) if i == 0 else eq.next_to(
                equations[i - 1], DOWN, aligned_edge=LEFT
            )
            self.play(Write(eq))
            self.wait(1)
