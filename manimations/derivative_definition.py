from manim import *
from sympy import symbols, latex, lambdify
import numpy as np


config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 10.0
config.frame_width = 18.0

# GLOBAL VARIABLES
x = symbols('x')
FUNC_EDITABLE = 0.5 * x**2 - x

X_RANGE_EDITABLE = [-5, 5, 1]
Y_RANGE_EDITABLE = [-5, 5, 1]
START_X_EDITABLE = 3
STATIONARY_X_EDITABLE = -2

# Easily editable function
lambda_func = lambdify(x, FUNC_EDITABLE, modules=['numpy'])
func_latex = f"f(x) = {latex(FUNC_EDITABLE)}"

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

        """rhs_derivative_def = MathTex(
            "= \\text{slope of the secant line}",
            font_size=36
        ).next_to(lhs_derivative_def, RIGHT)"""

        """explanation = Text(
            "As h → 0, the slope of the secant line approaches\nthe slope of the tangent line.",
            font_size=28
        ).next_to(lhs_derivative_def, DOWN, aligned_edge=LEFT)"""

        # Write both sides of the equation
        self.play(Write(lhs_derivative_def))
        

        func_label = MathTex(func_latex, font_size=36).to_corner(DL)
        self.play(Write(func_label))
        self.wait(1)


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
        func_curve = axes.plot(lambda_func, color=BLUE)
        self.play(Create(func_curve))

        # Stationary and moving points
        stationary_point = Dot(axes.c2p(STATIONARY_X_EDITABLE, lambda_func(STATIONARY_X_EDITABLE)), color=RED)
        moving_point = Dot(axes.c2p(START_X_EDITABLE, lambda_func(START_X_EDITABLE)), color=YELLOW)
        self.play(Create(stationary_point), Create(moving_point))

        # Labels next to each point
        stationary_label = Text(
            "(x, f(x))",
            font_size=28,
            color=WHITE
        ).next_to(stationary_point, UP, buff=0.3)

        moving_label = Text(
            "(x+h, f(x+h))",
            font_size=28,
            color=WHITE
        ).next_to(moving_point, UP, buff=0.3)

        self.play(Write(stationary_label))
        self.wait(1)
        self.play(Write(moving_label))


        # dotted lines
        x_line = DashedLine(start=stationary_point.get_center(), end=axes.c2p(STATIONARY_X_EDITABLE, 0), color=YELLOW)
        x_plus_h_line = DashedLine(start=moving_point.get_center(), end=axes.c2p(START_X_EDITABLE, 0), color=YELLOW)

        start_x_label = MathTex("x", font_size=32).next_to(axes.c2p(STATIONARY_X_EDITABLE, 0), DOWN, buff=0.2)
        start_x_plus_h_label = MathTex("x+h", font_size=32).next_to(axes.c2p(START_X_EDITABLE, 0), DOWN, buff=0.2)

                # Create a brace between x and x+h on the x-axis
        brace = Brace(
            Line(
                axes.c2p(STATIONARY_X_EDITABLE, 0),
                axes.c2p(START_X_EDITABLE, 0),
            ),
            direction=-UP
        )
        
        brace.shift(DOWN * 0.5)
        h_label = brace.get_text("h")

        # Slope formula
        slope_eq = MathTex(
            "\\text{slope} = \\frac{f(x+h) - f(x)}{(x+h) - x}",
            font_size=36
        ).to_corner(UL).shift(DOWN * 1.5)

        # Simplified slope
        slope_simplified = MathTex(
            "\\text{slope} = \\frac{f(x+h) - f(x)}{h}",
            font_size=36
        ).move_to(slope_eq.get_center())

        stationary_y = lambda_func(STATIONARY_X_EDITABLE)
        moving_y = lambda_func(START_X_EDITABLE)

        vertical_base_point = axes.c2p(START_X_EDITABLE, stationary_y)

        vertical_leg = Line(moving_point.get_center(), vertical_base_point, color=BLUE)
        horizontal_leg = Line(vertical_base_point, stationary_point.get_center(), color=GREEN)

        vertical_leg_label = MathTex("f(x+h)-f(x)", font_size=28).next_to(vertical_leg, RIGHT, buff=0.2)
        horizontal_leg_label = MathTex("h", font_size=28).next_to(horizontal_leg, UP, buff=0.2)



        slope_label = always_redraw(lambda: MathTex(
            "Slope =", f"{self.calculate_slope(STATIONARY_X_EDITABLE, self.get_x_coordinate(moving_point, axes)):.2f}"
        ).to_corner(DR))
        x_label = MathTex("x =" f"{STATIONARY_X_EDITABLE}").next_to(slope_label, UP, buff=0.5)
        self.play (Write(x_label))

        # Animate slope explanation
        self.play(Write(slope_eq))
        self.wait(1)
        self.play(Transform(slope_eq, slope_simplified))  # Skip copying the denominator part
        self.wait(2)


        self.play(Create(x_line), Create(x_plus_h_line), Write(start_x_label), Write(start_x_plus_h_label))
        self.play(Create(brace), Write(h_label))
        self.wait(2)
        self.play(FadeOut(x_line), FadeOut(x_plus_h_line), FadeOut(start_x_label), FadeOut(start_x_plus_h_label), FadeOut(brace), FadeOut(h_label), FadeOut(stationary_label), FadeOut(moving_label))

        self.wait(1)
        self.play(Create(vertical_leg), Create(horizontal_leg))
        self.play(Write(vertical_leg_label), Write(horizontal_leg_label))
        self.wait(2)
        self.play( FadeOut(vertical_leg), FadeOut(horizontal_leg), FadeOut(vertical_leg_label), FadeOut(horizontal_leg_label),FadeOut(slope_eq))

        tangent_line = always_redraw(lambda: self.get_tangent_line(axes, STATIONARY_X_EDITABLE))
        tangent_label = Text("Tangent line:", font_size=32).set_color(YELLOW).next_to(tangent_line, LEFT)
        tangent_label.shift(RIGHT * 3 + DOWN * 0.5)
        self.play(Create(tangent_line), Write(tangent_label))


        # Secant Line
        secant_line = always_redraw(lambda: self.get_extended_secant_line(
            axes, STATIONARY_X_EDITABLE, self.get_x_coordinate(moving_point, axes)
        ))
        self.play(Create(secant_line))

        # h line and label
        h_line = always_redraw(lambda: Line(
            axes.c2p(STATIONARY_X_EDITABLE, lambda_func(STATIONARY_X_EDITABLE)),
            axes.c2p(self.get_x_coordinate(moving_point, axes), lambda_func(STATIONARY_X_EDITABLE)),
            color=YELLOW
        ))
        h_label = MathTex("h =", f"{abs(self.get_x_coordinate(moving_point, axes) - STATIONARY_X_EDITABLE):.2f}")
        h_label.add_updater(lambda m: m.become(
            MathTex("h =", f"{abs(self.get_x_coordinate(moving_point, axes) - STATIONARY_X_EDITABLE):.2f}")
            .next_to(h_line, DOWN, buff=0.5)
            .set_opacity(self.compute_h_opacity(self.get_x_coordinate(moving_point, axes)))
        ))

        self.play(Create(h_line), Write(h_label))

        # Slope tracker
       
        self.play(Write(slope_label))
    
        # Path animation
        path_points = [axes.c2p(x, lambda_func(x)) for x in np.linspace(START_X_EDITABLE, STATIONARY_X_EDITABLE, 100)]
        path = VMobject().set_points_as_corners(path_points)
        self.play(MoveAlongPath(moving_point, path, rate_func=rate_functions.ease_out_sine, run_time=5))
        self.play(moving_point.animate.move_to(axes.c2p(STATIONARY_X_EDITABLE, lambda_func(STATIONARY_X_EDITABLE))), run_time=0.5)

        self.play(FadeOut(h_label), FadeOut(h_line))
        self.wait()


    def compute_h_opacity(self, x_val):
        h = abs(x_val - STATIONARY_X_EDITABLE)
        if h > 0.2:
            return 1  # fully visible
        elif h > 0.05:
            return (h - 0.05) / (0.15)  # fade out linearly from 1 to 0
        else:
            return 0  # fully invisible

    def get_x_coordinate(self, dot, axes):
        return axes.p2c(dot.get_center())[0]

    def calculate_derivative(self, x, dx=1e-4):
        return (lambda_func(x + dx) - lambda_func(x - dx)) / (2 * dx)

    def calculate_slope(self, x1, x2):
        if x1 == x2:
            return self.calculate_derivative(x1)
        y1 = lambda_func(x1)
        y2 = lambda_func(x2)
        return (y2 - y1) / (x2 - x1)
    
    def get_tangent_line(self, axes, x, dx=1e-4):
        slope = self.calculate_derivative(x, dx)
        y = lambda_func(x)

        delta_x = 5
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
            y1 = lambda_func(x1)
        else:
            y1 = lambda_func(x1)
            y2 = lambda_func(x2)
            slope = (y2 - y1) / (x2 - x1)

        x_min, x_max = X_RANGE_EDITABLE[0], X_RANGE_EDITABLE[1]
        y_min = y1 + slope * (x_min - x1)
        y_max = y1 + slope * (x_max - x1)

        return Line(
            axes.c2p(x_min, y_min),
            axes.c2p(x_max, y_max),
            color=GREEN
        )

    
