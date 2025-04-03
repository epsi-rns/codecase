from manim import *

# Define colors
CONFIG = {
    "color_bg": WHITE,
    "color_fg": BLACK,

    # Highlight important variables
    "color_hl": BLUE_E,

    # Final result in red
    "color_rs": RED_E
}

class InverseFunction(Scene):
    def construct(self):
        self.setup_scene()
        equations = self.get_equations()
        self.animate_equations(equations)

        # Highlight final result
        self.final_highlight(equations[-1])
        self.wait(2)

    def setup_scene(self):
        self.camera.background_color = CONFIG["color_bg"]

    def get_equations(self):
        return [
            MathTex(
                r"f(x) = \frac{2x}{4x - 7},"
                r" \quad x \neq \frac{7}{4}",
                color=CONFIG["color_hl"]
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
                # Highlight important change
                color=CONFIG["color_fg"]
            ),
            MathTex(
                r"\therefore \quad f(x)^{-1} = \frac{7x}{4x - 2},"
                r"\quad x \neq \frac{1}{2}",
                color=CONFIG["color_rs"]
            ),
        ]

    def animate_equations(self, equations):
        # Position first equation at the top
        # This forces it to the top
        equations[0].to_edge(UP)

        # Show first equation
        self.play(FadeIn(equations[0]))
        self.wait(0.8)

        for i in range(1, len(equations)):
            # Position new equation below the previous one
            equations[i].next_to(
                equations[i-1], DOWN, aligned_edge=LEFT)

            # Transform a copy of the previous equation
            # into the new one
            self.play(ReplacementTransform(
                equations[i-1].copy(), equations[i]))
            self.wait(0.8)

    def final_highlight(self, final_eq):
        self.play(
            # Scale + color change
            final_eq.animate.scale(1.2)\
                .set_color(CONFIG["color_hl"]),
            run_time=0.3
        )
        self.wait(0.3)
        self.play(
            # Revert
            final_eq.animate.scale(1/1.2)\
                .set_color(CONFIG["color_rs"]),
            run_time=0.3
        )
        self.wait(0.5)

