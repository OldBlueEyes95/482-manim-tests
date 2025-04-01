from manim import *
import numpy as np

config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 10.0
config.frame_width = 18.0

# GLOBAL VARIABLES
X_RANGE_EDITABLE = [-5, 5, 1]
Y_RANGE_EDITABLE = [-5, 5, 1]
START_X = 2  # Initial x position for moving point
STATIONARY_X = -3  # x position of the stationary point

class DerivativeDefinition(Scene):
    def construct(self):
        # Definition of the derivative (top left corner)
        derivative_def = MathTex(
            "f'(x) = \\lim\\limits_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            font_size=36
        ).to_corner(UL)
        self.play(Write(derivative_def))

        # Axes
        axes = Axes(
            x_range=X_RANGE_EDITABLE,
            y_range=Y_RANGE_EDITABLE,
            axis_config={"color": WHITE},
            tips=False  
        )
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes), Write(labels))

        # Function
        func = axes.plot(lambda x: 0.1 * x**3 - 0.5 * x, color=BLUE)
        self.play(Create(func))

        # Stationary point
        stationary_point = Dot(axes.c2p(STATIONARY_X, 0.1 * STATIONARY_X**3 - 0.5 * STATIONARY_X), color=RED)
        self.play(Create(stationary_point))

        # Moving point
        moving_point = Dot(axes.c2p(START_X, 0.1 * START_X**3 - 0.5 * START_X), color=YELLOW)
        self.play(Create(moving_point))

        # Secant Line (updates dynamically)
        secant_line = always_redraw(lambda: self.get_extended_secant_line(
            axes, STATIONARY_X, self.get_x_coordinate(moving_point, axes)
        ))
        self.play(Create(secant_line))

        # Initial h-line
        h_line = always_redraw(lambda: Line(
            axes.c2p(STATIONARY_X, 0.1 * STATIONARY_X**3 - 0.5 * STATIONARY_X),
            axes.c2p(self.get_x_coordinate(moving_point, axes), 0.1 * STATIONARY_X**3 - 0.5 * STATIONARY_X),
            color=YELLOW
        ))
        self.play(Create(h_line))

        # h Label (updating with movement)
        h_label = always_redraw(lambda: MathTex(
            "h =", f"{abs(self.get_x_coordinate(moving_point, axes) - STATIONARY_X):.2f}"
        ).next_to(h_line, DOWN, buff=0.5))

        self.play(Write(h_label))

        # Slope tracker label (fixed in lower right)
        slope_label = always_redraw(lambda: MathTex(
            "Slope =", f"{self.calculate_slope(STATIONARY_X, self.get_x_coordinate(moving_point, axes)):.2f}"
        ).to_corner(DR))

        self.play(Write(slope_label))

        # Path for moving point (from Start_X to Stationary_X)
        path_points = [
            axes.c2p(x, 0.1 * x**3 - 0.5 * x) for x in np.linspace(START_X, STATIONARY_X, 100)
        ]
        path = VMobject().set_points_as_corners(path_points)

        # Animate the moving point
        self.play(
            MoveAlongPath(moving_point, path, rate_func=linear, run_time=5),
        )

        # Ensure moving point stops exactly at stationary point
        self.play(moving_point.animate.move_to(axes.c2p(STATIONARY_X, 0.1 * STATIONARY_X**3 - 0.5 * STATIONARY_X)), run_time=0.5)

        # Final tangent slope label
        final_slope = self.calculate_derivative(STATIONARY_X)
        tangent_slope_label = MathTex(f"Slope = {final_slope:.2f}").to_corner(DR)
        #self.play(Transform(slope_label, tangent_slope_label))

        # Remove h label and h-line
        self.play(FadeOut(h_label), FadeOut(h_line))

        self.wait()

    def get_x_coordinate(self, dot, axes):
        return axes.p2c(dot.get_center())[0]

    def calculate_derivative(self, x):
        return 0.3 * x**2 - 0.5

    def calculate_slope(self, x1, x2):
        if x1 == x2:
            return self.calculate_derivative(x1)
        y1 = 0.1 * x1**3 - 0.5 * x1
        y2 = 0.1 * x2**3 - 0.5 * x2
        return (y2 - y1) / (x2 - x1)

    def get_extended_secant_line(self, axes, x1, x2):
        if x1 == x2:
            slope = self.calculate_derivative(x1)
            y1 = 0.1 * x1**3 - 0.5 * x1
            x_min, x_max = X_RANGE_EDITABLE[0], X_RANGE_EDITABLE[1]
            y_min = y1 + slope * (x_min - x1)
            y_max = y1 + slope * (x_max - x1)
        else:
            y1 = 0.1 * x1**3 - 0.5 * x1
            y2 = 0.1 * x2**3 - 0.5 * x2
            slope = (y2 - y1) / (x2 - x1)
            x_min, x_max = X_RANGE_EDITABLE[0], X_RANGE_EDITABLE[1]
            y_min = y1 + slope * (x_min - x1)
            y_max = y1 + slope * (x_max - x1)

        return Line(
            axes.c2p(x_min, y_min),
            axes.c2p(x_max, y_max),
            color=GREEN
        )
