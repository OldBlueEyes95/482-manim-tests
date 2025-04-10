from manim import *
import numpy as np

config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 10.0
config.frame_width = 18.0

# GLOBAL VARIABLES
X_RANGE_EDITABLE = [-5, 5, 1]
Y_RANGE_EDITABLE = [-5, 5, 1]
START_X_EDITABLE = 2
STATIONARY_X_EDITABLE = -1

# Easily editable function
FUNC_EDITABLE = lambda x: 0.5 * x**2 - x



class DerivativeDefinition(Scene):
    def construct(self):
        title = Text("Derivative Definition", font_size=60).set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Derivative definition with explanation
        lhs_derivative_def = MathTex(
            "f'(x) = \\lim\\limits_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            font_size=36
        ).to_corner(UL)

        rhs_derivative_def = MathTex(
            "= \\text{slope of the secant line}",
            font_size=36
        ).next_to(lhs_derivative_def, RIGHT)

        explanation = Text(
            "As h → 0, the slope of the secant line approaches\nthe slope of the tangent line.",
            font_size=28
        ).next_to(lhs_derivative_def, DOWN, aligned_edge=LEFT)

        # Write both sides of the equation
        self.play(Write(lhs_derivative_def), Write(rhs_derivative_def))
        self.wait(1)
        self.play(Write(explanation))
        self.wait(2)
        # Fade out only the right-hand side and explanation
        self.play(FadeOut(rhs_derivative_def), FadeOut(explanation))


        # Axes
        axes = Axes(
            x_range=X_RANGE_EDITABLE,
            y_range=Y_RANGE_EDITABLE,
            axis_config={"color": WHITE},
            tips=False
        )
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes), Write(labels))

        # Function curve
        func_curve = axes.plot(FUNC_EDITABLE, color=BLUE)
        self.play(Create(func_curve))

        # Stationary and moving points
        stationary_point = Dot(axes.c2p(STATIONARY_X_EDITABLE, FUNC_EDITABLE(STATIONARY_X_EDITABLE)), color=RED)
        moving_point = Dot(axes.c2p(START_X_EDITABLE, FUNC_EDITABLE(START_X_EDITABLE)), color=YELLOW)
        self.play(Create(stationary_point), Create(moving_point))


        
        tangent_line = always_redraw(lambda: self.get_tangent_line(axes, STATIONARY_X_EDITABLE))
        tangent_label = Text("Tangent line:", font_size=32).set_color(YELLOW).next_to(tangent_line, LEFT)
        tangent_label.shift(RIGHT * 1.5 + DOWN * 0.5)
        self.play(Create(tangent_line), Write(tangent_label))


        # Secant Line
        secant_line = always_redraw(lambda: self.get_extended_secant_line(
            axes, STATIONARY_X_EDITABLE, self.get_x_coordinate(moving_point, axes)
        ))
        self.play(Create(secant_line))

        # h line and label
        h_line = always_redraw(lambda: Line(
            axes.c2p(STATIONARY_X_EDITABLE, FUNC_EDITABLE(STATIONARY_X_EDITABLE)),
            axes.c2p(self.get_x_coordinate(moving_point, axes), FUNC_EDITABLE(STATIONARY_X_EDITABLE)),
            color=YELLOW
        ))
        h_label = always_redraw(lambda: MathTex(
            "h =", f"{abs(self.get_x_coordinate(moving_point, axes) - STATIONARY_X_EDITABLE):.2f}"
        ).next_to(h_line, DOWN, buff=0.5))
        self.play(Create(h_line), Write(h_label))

        # Slope tracker
        slope_label = always_redraw(lambda: MathTex(
            "Slope =", f"{self.calculate_slope(STATIONARY_X_EDITABLE, self.get_x_coordinate(moving_point, axes)):.2f}"
        ).to_corner(DR))
        x_label = MathTex("x =" f"{STATIONARY_X_EDITABLE}").next_to(slope_label, UP, buff=0.5)
        self.play(Write(slope_label), Write(x_label))

        # Path animation
        path_points = [axes.c2p(x, FUNC_EDITABLE(x)) for x in np.linspace(START_X_EDITABLE, STATIONARY_X_EDITABLE, 100)]
        path = VMobject().set_points_as_corners(path_points)
        self.play(MoveAlongPath(moving_point, path, rate_func=rate_functions.ease_out_sine, run_time=5))
        self.play(moving_point.animate.move_to(axes.c2p(STATIONARY_X_EDITABLE, FUNC_EDITABLE(STATIONARY_X_EDITABLE))), run_time=0.5)

        self.play(FadeOut(h_label), FadeOut(h_line))
        self.wait()

    def get_x_coordinate(self, dot, axes):
        return axes.p2c(dot.get_center())[0]

    def calculate_derivative(self, x, dx=1e-4):
        return (FUNC_EDITABLE(x + dx) - FUNC_EDITABLE(x - dx)) / (2 * dx)

    def calculate_slope(self, x1, x2):
        if x1 == x2:
            return self.calculate_derivative(x1)
        y1 = FUNC_EDITABLE(x1)
        y2 = FUNC_EDITABLE(x2)
        return (y2 - y1) / (x2 - x1)
    
    def get_tangent_line(self, axes, x, dx=1e-4):
        slope = self.calculate_derivative(x, dx)
        y = FUNC_EDITABLE(x)

        delta_x = 1.5
        x1 = x - delta_x
        x2 = x + delta_x
        y1 = y + slope * (x1 - x)
        y2 = y + slope * (x2 - x)

        return Line(
            axes.c2p(x1, y1),
            axes.c2p(x2, y2),
            color=YELLOW,
            stroke_width=4
        )

    def get_extended_secant_line(self, axes, x1, x2):
        if abs(x1 - x2) < 1e-6:
            slope = self.calculate_derivative(x1)
            y1 = FUNC_EDITABLE(x1)
        else:
            y1 = FUNC_EDITABLE(x1)
            y2 = FUNC_EDITABLE(x2)
            slope = (y2 - y1) / (x2 - x1)

        x_min, x_max = X_RANGE_EDITABLE[0], X_RANGE_EDITABLE[1]
        y_min = y1 + slope * (x_min - x1)
        y_max = y1 + slope * (x_max - x1)

        return Line(
            axes.c2p(x_min, y_min),
            axes.c2p(x_max, y_max),
            color=GREEN
        )

    
