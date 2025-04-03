from manim import *

class InverseFunction(Scene):
    def construct(self):
        # Define the equations step by step
        equations = [
            MathTex(r"f(x) = \frac{2x}{4x - 7}, \quad x \neq \frac{7}{4}"),
            MathTex(r"\Rightarrow \quad y = \frac{2x}{4x - 7}"),
            MathTex(r"\Rightarrow \quad 4xy - 7y = 2x"),
            MathTex(r"\Rightarrow \quad 4xy - 2x = 7y"),
            MathTex(r"\Rightarrow \quad x(4y - 2) = 7y"),
            MathTex(r"\Rightarrow \quad x = \frac{7y}{4y - 2}"),
            MathTex(r"\therefore \quad f(x)^{-1} = \frac{7x}{4x - 2}, \quad x \neq \frac{1}{2}"),
        ]

        # Positioning equations sequentially
        for i, eq in enumerate(equations):
            eq.to_edge(UP) if i == 0 else eq.next_to(equations[i-1], DOWN, aligned_edge=LEFT)

        # Animate equations appearing one by one
        for eq in equations:
            self.play(Write(eq))
            self.wait(1)

        self.wait(2)
