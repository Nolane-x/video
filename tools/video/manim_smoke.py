from manim import *

class VideoToolchainProof(Scene):
    def construct(self):
        title = Text("A function tells a story", font_size=34).to_edge(UP)
        axes = Axes(x_range=[-3, 3, 1], y_range=[-1, 5, 1], x_length=7, y_length=3.6, tips=False).shift(DOWN * 0.35)
        graph = axes.plot(lambda x: x**2 / 2, x_range=[-2.8, 2.8], color=BLUE)
        equation = MathTex(r"y=\frac{x^2}{2}").scale(0.9).next_to(axes, DOWN, buff=0.25)
        self.play(Write(title))
        self.play(Create(axes), run_time=1.2)
        self.play(Create(graph), run_time=1.8)
        self.play(Write(equation), run_time=0.8)
        self.wait(1)
