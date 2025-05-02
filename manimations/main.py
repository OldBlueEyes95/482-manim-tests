from manim import *
import sympy
from sympy.parsing.latex import parse_latex
import csv
from typing import List

MANIM_SCREEN_WIDTH  = 14.00  # Full screen width: -7 to 7
MANIM_SCREEN_HEIGHT =  5.33  # Top 2/3rds height: 4 to -4/3

MATRIX_A_ROW_END_HEIGHT = -2.00
MATRIX_B_COL_END_DIFF   =  1.00

def csv_to_matrix(file_name, assert_square=True) -> List[List[str]]:
    with open(file_name) as matrix_file:
        reader = csv.reader(matrix_file, delimiter=',')
        row_length = None
        
        matrix = []
        for row in reader:
            if row_length is None:
                row_length = len(row)
            assert len(row) == row_length, "Matrix rows must all be the same length.\n"
            matrix.append(row)
        
        if assert_square:
            assert len(matrix) == row_length, "Matrix must be square."
    
    #TODO add LaTeX validation here
    
    return matrix


def symbolic_multiply(
    mA: List[List[str]],
    mB: List[List[str]],
    write_to_file=False
) -> None:
    m: int = len(mA)    # rows of A
    n: int = len(mA[0]) # cols of A OR len(matrix_B) aka rows of B
    r: int = len(mB[0]) # cols of B
    
    sA: List[List[sympy.Expr]] = [
        [parse_latex(e, strict=False, backend='antlr') for e in row] for row in mA
    ]
    sB: List[List[sympy.Expr]] = [
        [parse_latex(e, strict=False, backend='antlr') for e in row] for row in mB
    ]
    
    iO: List[List[List[str]]] = [[] for _ in range(m)] # intermediate row additions
    fO: List[List[      str]] = [[] for _ in range(m)] # final results
    
    for row in range(m):
        for col in range(r):
            multiplied_elements = [sA[row][i] * sB[i][col] for i in range(n)]
            
            if write_to_file:
                for element in multiplied_elements:
                    print(element)
            
            iO[row].append([sympy.latex(product) for product in multiplied_elements])
            fO[row].append(sympy.latex(sum(multiplied_elements)))
    
    return iO, fO


class GenericMatrixMultiply(Scene):
    # def __init__(self):
    #     # Initialize the parent class (Shape) with color
    #     super().__init__()
    
    def construct(self):
        matrix_A = csv_to_matrix('matrixA.csv')
        matrix_B = csv_to_matrix('matrixB.csv')
        
        m: int = len(matrix_A)    # rows of A
        n: int = len(matrix_A[0]) # cols of A OR len(matrix_B) aka rows of B
        r: int = len(matrix_B[0]) # cols of B
        
        #TODO instead of this being an assert, animate a failure case where it fails to produce matrix_O and ends the video early
        assert n == len(matrix_B), "Matrices shapes do not align."
        
        matrix_I, matrix_F = symbolic_multiply(matrix_A, matrix_B)
        matrix_O = [['?' for _ in range(r)] for _ in range(m)]
        
        mA = Matrix(
            matrix_A,
            #TODO add dynamic vertical and horizontal spacing based on LaTeX elements
            left_bracket=r"(",
            right_bracket=r")"
        ).set_row_colors([RED_A, RED], GREEN, BLUE)
        mB = Matrix(
            matrix_B,
            left_bracket=r"(",
            right_bracket=r")"
        ).set_column_colors([RED_A, RED], GREEN_B, BLUE_B)
        mO = Matrix(
            matrix_O,
            left_bracket=r"(",
            right_bracket=r")"
        )
        
        g = Group(
            mA, 
            MathTex(r"\cdot").scale(1.5),
            mB,
            MathTex(r"=").scale(1.5),
            mO
        ).arrange(RIGHT, buff=0.5)
        
        # need to scale matrices to always fit
        width_scale = MANIM_SCREEN_WIDTH / g.width
        height_scale = MANIM_SCREEN_HEIGHT / g.height
        scale_factor = min(width_scale, height_scale) * 0.9  # 0.9 for a small margin
        
        # Apply scaling and position
        g.scale(scale_factor)
        g.move_to(UP * 1.33)  # Center in top 2/3rds
        
        g.move_to(UP * 1.33)
        
        self.add(g)
        self.wait(1)
        
        row_bar = SurroundingRectangle(mA.get_rows()[0])
        col_bar = SurroundingRectangle(mB.get_columns()[0])
        out_box = SurroundingRectangle(mO.get_rows()[0][0])
        
        for row_A in range(m):
            # render box around rows of A
            if row_A == 0:
                self.play(
                    FadeIn(row_bar)
                    # FadeIn(col_bar),
                    # FadeIn(out_box)
                )
            else:
                new_row_bar = SurroundingRectangle(mA.get_rows()[row_A])
                new_col_bar = SurroundingRectangle(mB.get_columns()[0])
                new_out_box = SurroundingRectangle(mO.get_rows()[row_A][0])
                self.play(
                    Transform(row_bar, new_row_bar),
                    Transform(col_bar, new_col_bar),
                    Transform(out_box, new_out_box)
                )
            
            self.wait(1)
            
            for col_B in range(r):
                # render box around cols of B
                if row_A == 0 and col_B == 0:
                    self.play(FadeIn(col_bar))
                else:
                    new_col_bar = SurroundingRectangle(mB.get_columns()[col_B])
                    self.play(Transform(col_bar, new_col_bar))
                
                # render box around element of O
                if row_A == 0 and col_B == 0:
                    self.play(FadeIn(out_box))
                elif col_B != 0:
                    new_out_box = SurroundingRectangle(mO.get_rows()[row_A][col_B])
                    self.play(Transform(out_box, new_out_box))
                
                #TODO fade out or move bounding box so its not in the way
                
                # do the multiplication
                self.wait(1)
                
                # row_elements = mA.get_rows()
                # col_elements = mB.get_columns()
                
                # for i in range(n):
                #     row_elements[i].animate.move_to((i-0.1, -MANIM_SCREEN_HEIGHT/6))
                #     col_elements[i].animate.move_to((i-0.1, -MANIM_SCREEN_HEIGHT/6 - 0.1))
                
                row_vals = mA.get_rows()[row_A].copy()
                col_vals = mB.get_columns()[col_B].copy()
                
                
                self.play(
                    row_vals.animate.move_to((0, MATRIX_A_ROW_END_HEIGHT, 0)),
                    col_vals.animate.rotate(PI/2).move_to((0, MATRIX_A_ROW_END_HEIGHT - MATRIX_B_COL_END_DIFF, 0))
                )
                self.play(
                    AnimationGroup([Rotate(element, -PI/2) for element in col_vals]),
                    Wait(3.0)
                )
                
                # since these objects aren't natively matrices, need to wrap in extra []
                combined_vector = Matrix(
                    [matrix_I[row_A][col_B]],
                    left_bracket=r"\langle",
                    right_bracket=r"\rangle",
                ).move_to((0, -2.15, 0))
                result = MathTex(matrix_F[row_A][col_B],).move_to((0, MATRIX_A_ROW_END_HEIGHT - MATRIX_B_COL_END_DIFF/2, 0))
                # Matrix(
                #     [[]],
                #     left_bracket=r"\langle",
                #     right_bracket=r"\rangle"
                # ).move_to((0, -2.15, 0))
                
                self.play(
                    Transform(Group(row_vals, col_vals), combined_vector, replace_mobject_with_target_in_scene=True),
                    Wait(2.0)
                )
                self.play(
                    Transform(combined_vector, result, replace_mobject_with_target_in_scene=True),
                    Wait(2.0)
                )
                self.play(
                    Swap(result, mO.get_entries()[row_A*m + col_B])
                )
                
                self.play(FadeOut(mO.get_entries()[row_A*m + col_B]))
        
        self.play(FadeOut(row_bar))
        self.play(FadeOut(col_bar))
        self.play(FadeOut(out_box))


# Credits to abul4fia for the camera fix (https://gist.github.com/abul4fia/1419b181e8e3410ef78e6acc25c3df94)
class MyCamera(ThreeDCamera):
    def transform_points_pre_display(self, mobject, points):
        if getattr(mobject, "fixed", False):
            return points
        else:
            return super().transform_points_pre_display(mobject, points)

class MyThreeDScene(ThreeDScene):
    def __init__(self, camera_class=MyCamera, ambient_camera_rotation=None,
                 default_angled_camera_orientation_kwargs=None, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)

def make_fixed(*mobs):
    for mob in mobs:
        mob.fixed = True
        for submob in mob.family_members_with_points():
            submob.fixed = True


def apply_colors(formula, colors) -> None:
    if len(colors) != 0:
        if len(colors) < len(formula):
            colors.extend([WHITE for _ in range(len(formula) - len(colors))])
        
        for i in range(len(formula)):
            formula[i].set_color(colors[i])


class CylindricalShells(MyThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        axes_range = [-5, 5, 1]
        standing_axes = ThreeDAxes(
            x_range=axes_range, y_range=axes_range, z_range=axes_range
        ).move_to(ORIGIN)
        # we lie about the axes: internally y is depth and z is height, but the student expects y as height and z as depth
        axes_labels = standing_axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("z-axis").scale(0.45), Text("y-axis").scale(0.45)
        )
        
        self.add(standing_axes, axes_labels)
        
        #TODO stretch goal: add a flat side image of the function in 2D space
        
        # Curve and Surface Config
        t_range = [0, 5]
        u_range = t_range
        v_range = [0, 2 * PI]
        resolution = (20, 40)
        fill_opacity = 0.7
        formula_font_size = 28
        
        # Constant function
        f_const = ParametricFunction(
            lambda t: np.array([t, 0, 1]),  # y=0, z=1 (constant height)
            t_range, color=RED
        ).set_shade_in_3d(True)
        s_const = Surface(
            lambda u, v: np.array([u, 1 * np.cos(v), 1 * np.sin(v)]),
            u_range=u_range, v_range=v_range, resolution=resolution,
            checkerboard_colors=[RED, RED_D],
            fill_opacity=fill_opacity
        )
        e_const_rstrs =  [r"V",  r"=", r"\pi", r"\int_a^b",    r"[1]^2", r"dx"]
        e_const_colors = [BLUE, WHITE,    RED,       GREEN,      YELLOW, GREEN]
        e_const = MathTex(*e_const_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        make_fixed(e_const)
        apply_colors(e_const, e_const_colors)
        
        e_const_final_rstrs =  [r"V",  r"=", r"\pi", r"[1]^2",  r"x"]
        e_const_final_colors = [BLUE, WHITE,    RED,   YELLOW, GREEN]
        e_const_final = MathTex(*e_const_final_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        make_fixed(e_const_final)
        apply_colors(e_const_final, e_const_final_colors)
        
        # Linear function
        f__line = ParametricFunction(
            lambda t: np.array([t, 0, 0.5 * t]),  # z = 0.5x
            t_range=t_range, color=BLUE
        ).set_shade_in_3d(True)
        s__line = Surface(
            lambda u, v: np.array([u, 0.5 * u * np.cos(v), 0.5 * u * np.sin(v)]),
            u_range=u_range, v_range=v_range, resolution=resolution,
            checkerboard_colors=[BLUE, BLUE_D],
            fill_opacity=fill_opacity
        )
        e__line_rstrs =  [r"V",  r"=", r"\pi", r"\int_a^b",    r"x^2", r"dx"]
        e__line_colors = [BLUE, WHITE,    RED,       GREEN,      YELLOW, GREEN]
        e__line = MathTex(*e__line_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        make_fixed(e__line)
        apply_colors(e__line, e__line_colors)
        
        e__line_final_rstrs =  [r"V",  r"=", r"\pi", r"\frac{1}{3} x^3"]
        e__line_final_colors = [BLUE, WHITE,    RED,            GREEN_C]
        e__line_final = MathTex(*e__line_final_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        make_fixed(e__line_final)
        apply_colors(e__line_final, e__line_final_colors)
        
        # Cubic function
        f_cubic = ParametricFunction(
            lambda t: np.array([t, 0, 0.02 * t**3]),  # z = 0.1x^3
            t_range=t_range, color=GREEN
        ).set_shade_in_3d(True)
        s_cubic = Surface(
            lambda u, v: np.array([u, 0.02 * u**3 * np.cos(v), 0.02 * u**3 * np.sin(v)]),
            u_range=u_range, v_range=v_range, resolution=resolution,
            checkerboard_colors=[GREEN, GREEN_D],
            fill_opacity=fill_opacity
        )
        e_cubic_rstrs =  [r"V",  r"=", r"\pi", r"\int_a^b",    r"[x^3]^2", r"dx"]
        e_cubic_colors = [BLUE, WHITE,    RED,       GREEN,      YELLOW, GREEN]
        e_cubic = MathTex(*e_cubic_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        make_fixed(e_cubic)
        apply_colors(e_cubic, e_cubic_colors)
        
        e_cubic_final_rstrs =  [r"V",  r"=", r"\pi", r"\frac{1}{7} x^7"]
        e_cubic_final_colors = [BLUE, WHITE,    RED,            GREEN_C]
        e_cubic_final = MathTex(*e_cubic_final_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        make_fixed(e_cubic_final)
        apply_colors(e_cubic_final, e_cubic_final_colors)
        
        
        cylinder_formula_rstrs =  [r"V_{ \text{Cylinder} }", r"=", r"\pi", r"r^2",  r"h"]
        cylinder_formula_colors = [                    BLUE, WHITE,   RED, YELLOW, GREEN]
        cylinder_formula_tex = MathTex(
            *cylinder_formula_rstrs,
            font_size=formula_font_size
        ).to_corner(UR, buff=0.5)
        
        make_fixed(cylinder_formula_tex) # replaces `self.add_fixed_in_frame_mobjects()`
        apply_colors(cylinder_formula_tex, cylinder_formula_colors)
        # for i in range(len(cylinder_formula_rstrs)):
        #     cylinder_formula_tex[i].set_color(cylinder_formula_colors[i])
        
        shell_formula_rstrs =  [r"V",  r"=", r"\pi", r"\int_a^b", r"[f(x)]^2", r"dx"]
        shell_formula_colors = [BLUE, WHITE,    RED,       GREEN,      YELLOW, GREEN]
        shell_formula_tex = MathTex(
            *shell_formula_rstrs,
            font_size=formula_font_size
        ).to_corner(UR, buff=0.5)
        
        make_fixed(shell_formula_tex) # replaces `self.add_fixed_in_frame_mobjects()`
        apply_colors(shell_formula_tex, shell_formula_colors)
        # for i in range(len(shell_formula_rstrs)):
        #     shell_formula_tex[i].set_color(shell_formula_colors[i])
        
        
        # Render all of the predefined formulas and shapes
        # const
        self.play(Write(f_const))
        self.play(
            Rotate(f_const, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s_const, rate_func=rate_functions.linear)
        )
        self.wait(1)
        
        
        self.play(Write(cylinder_formula_tex))
        self.play(TransformMatchingTex(cylinder_formula_tex, shell_formula_tex, run_time=3))
        self.wait(1)
        self.play(TransformMatchingTex(shell_formula_tex, e_const))
        self.play(TransformMatchingTex(e_const, e_const_final))
        self.play(FadeOut(f_const, s_const, e_const_final))
        
        # line
        self.play(Write(f__line))
        self.play(
            Rotate(f__line, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s__line, rate_func=rate_functions.linear)
        )
        self.wait(1)
        
        self.play(Write(shell_formula_tex))
        self.play(TransformMatchingTex(shell_formula_tex, e__line))
        self.play(TransformMatchingTex(e__line, e__line_final))
        
        self.play(FadeOut(f__line, s__line, e__line_final))
        
        # cubic
        self.play(Write(f_cubic))
        self.play(
            Rotate(f_cubic, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s_cubic, rate_func=rate_functions.linear)
        )
        self.wait(1)
        
        self.play(Write(shell_formula_tex))
        self.play(TransformMatchingTex(shell_formula_tex, e_cubic))
        self.play(TransformMatchingTex(e_cubic, e_cubic_final))
        
        self.play(FadeOut(f_cubic, s_cubic, e_cubic_final))
        
        
        self.wait(1)


class ConeDebugging(Scene):
    def construct(self):
        # Step 2: Problem Statement
        REAL_HEIGHT_EDITABLE = 20
        REAL_RADIUS_EDITABLE = 6
        VOLUME_LOSS_EDITABLE = 15
        SCALE_FACTOR_EDITABLE = 0.25
        PLAYBACK_SPEED_EDITABLE = 8
        #change to use REAL_HEIGHT_EDITABLE and REAL_RADIUS_EDITABLE in the problem statement
        problem_strs = [
            r"An inverted cone has a height of ",
            f"{REAL_HEIGHT_EDITABLE}",
            r"cm and a radius of ",
            f"{REAL_RADIUS_EDITABLE}",
            r"cm, and was initially full of water.",
            "\n",
            r"The water drains out at a rate of ",
            f"{VOLUME_LOSS_EDITABLE} ",
            r"cm$^3$/sec.",
            "\n",
            "The surface level of the water falls as a result. ",
            "At what rate is the water level falling when the water is halfway down the cone?"
        ]
        problem_statement = Tex(*problem_strs, font_size=20).to_edge(UP)
        self.add(problem_statement)


from math import gcd

# Set the resolution and frame size
config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 10.0
config.frame_width = 18.0

class ConeRelatedRates(Scene):
    def construct(self):
        # Step 1: Title Screen
        title = Text("Related Rates Cone Problem", font_size=60).set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Step 2: Problem Statement
        REAL_HEIGHT_EDITABLE = 20
        REAL_RADIUS_EDITABLE = 6
        VOLUME_LOSS_EDITABLE = 15
        SCALE_FACTOR_EDITABLE = 0.25
        PLAYBACK_SPEED_EDITABLE = 8
        #change to use REAL_HEIGHT_EDITABLE and REAL_RADIUS_EDITABLE in the problem statement
        problem_strs = [
            r"An inverted cone has a height of ",
            f"{REAL_HEIGHT_EDITABLE}",
            r"cm and a radius of ",
            f"{REAL_RADIUS_EDITABLE}",
            r"cm, and was initially full of water.",
            "\n",
            r"The water drains out at a rate of ",
            f"{VOLUME_LOSS_EDITABLE} ",
            r"cm$^3$/sec.",
            "\n",
            "The surface level of the water falls as a result. ",
            "At what rate is the water level falling when the water is halfway down the cone?"
        ]
        problem_statement = Tex(*problem_strs, font_size=20).to_edge(UP)
        self.play(Write(problem_statement))
        self.wait(2)

        # Step 3: Create the cone
        
        cone_height = REAL_HEIGHT_EDITABLE * SCALE_FACTOR_EDITABLE
        cone_radius = REAL_RADIUS_EDITABLE * SCALE_FACTOR_EDITABLE
        cone = Cone(height=cone_height, base_radius=cone_radius, direction=DOWN, checkerboard_colors=False).shift(DOWN * 2)
        cone.set_fill(opacity=0.3)

        self.play(Create(cone))
        self.wait(1)

        # Step 4: Create the water level
        water = cone.copy().set_fill(BLUE, opacity=0.8)
        self.play(Create(water))
        self.wait(1)

        # Step 5: Add initial lines for radius and height with labels
        height_line = Line(cone.get_top(), cone.get_bottom(), color=YELLOW_E)
        #Use REAL_HEIGHT_EDITABLE and REAL_RADIUS_EDITABLE for the labels
        height_label = MathTex(f"{REAL_HEIGHT_EDITABLE}\\text{{ cm}}").next_to(height_line, RIGHT, buff=0.1)
        radius_line = Line(cone.get_top(), cone.get_top() + RIGHT * cone_radius, color=YELLOW_E)
        radius_label = MathTex(f"{REAL_RADIUS_EDITABLE}\\text{{ cm}}").next_to(radius_line, UP, buff=0.1)

        self.play(Create(height_line), Write(height_label), Create(radius_line), Write(radius_label))
        self.wait(1)

        # Fade out initial lines and labels as the water starts to fall
        self.play(FadeOut(height_line), FadeOut(height_label), FadeOut(radius_line), FadeOut(radius_label))

        # Explain how halfway height is calculated
        height_explanation_text = Text(
            f"Total height = {REAL_HEIGHT_EDITABLE} cm\nHalfway height = {REAL_HEIGHT_EDITABLE} / 2 = {REAL_HEIGHT_EDITABLE / 2} cm",
            font_size=24
        ).to_edge(LEFT).shift(UP * 2)

        self.play(Write(height_explanation_text))
        self.wait(2)
        self.play(FadeOut(height_explanation_text))


        # Add halfway marker
        halfway_line = DashedLine(cone.get_bottom() + RIGHT * cone_radius, cone.get_top() + DOWN * (cone_height / 2) + RIGHT * cone_radius, color=YELLOW)
        #Use half of REAL_HEIGHT_EDITABLE for halfway_text
        halfway_text = MathTex(f"h ={REAL_HEIGHT_EDITABLE / 2}\\text{{ cm}}", font_size=24).next_to(halfway_line, RIGHT)
        self.play(Create(halfway_line), Write(halfway_text))

        # Define an accelerating drain function
        def accelerating_drain(t):
            term = cone_height ** 3 - (3 * VOLUME_LOSS_EDITABLE * cone_height ** 2 / (np.pi * cone_radius ** 2)) * t
            h_t = term ** (1 / 3) if term > 0 else 0  # Prevent complex numbers
            return h_t


        def update_water(mob, alpha):
            """Gradually shrink water cone while maintaining similarity and alignment."""
            new_height = max(accelerating_drain(alpha), 1e-6)
            new_radius = (cone_radius / cone_height) * new_height
            mob.become(Cone(height=new_height, base_radius=new_radius, direction=DOWN))
            mob.set_fill(BLUE, opacity=0.75)
            mob.shift(DOWN * 2)

        self.play(UpdateFromAlphaFunc(water, update_water), run_time=PLAYBACK_SPEED_EDITABLE)
        self.wait(2)


        # Step 7: Add new lines for the halfway radius and height with labels
        #Again, use REAL_HEIGHT_EDITABLE and REAL_RADIUS_EDITABLE for the labels
        new_height_line = Line(cone.get_top() + DOWN * (cone_height / 2), cone.get_bottom(), color=YELLOW_E)
        new_height_label = MathTex(f"{REAL_HEIGHT_EDITABLE / 2}\\text{{ cm}}").next_to(new_height_line, RIGHT, buff=0.1)

        new_radius_line = Line(cone.get_top() + DOWN * (cone_height / 2), cone.get_top() + DOWN * (cone_height / 2) + RIGHT * (cone_radius / 2), color=YELLOW_E)
        new_radius_label = MathTex(f"{REAL_RADIUS_EDITABLE / 2}\\text{{ cm}}").next_to(new_radius_line, UP, buff=0.1)

        self.play(Create(new_height_line), Write(new_height_label), Create(new_radius_line), Write(new_radius_label))

        self.wait(1)

        # Step 8: Fade out the second set of lines
        self.play(FadeOut(halfway_text), FadeOut(halfway_line))
        self.play(FadeOut(new_height_line), FadeOut(new_height_label), FadeOut(new_radius_line), FadeOut(new_radius_label))

        # Step 9: Move both cones to the left
        self.play(cone.animate.shift(LEFT * 5), water.animate.shift(LEFT * 5))

        half_cone = Cone(height=cone_height / 2, base_radius=cone_radius / 2, direction=DOWN, checkerboard_colors=False).set_fill(BLUE, opacity=0.8).shift(DOWN * 2 + LEFT * 5)
        self.play(FadeIn(half_cone))

        self.wait(1)

        # Step 10: Work through the problem
        known_values = MathTex(r"\frac{dV}{dt} = -" + str(VOLUME_LOSS_EDITABLE) + r"\, \text{cm}^3/\text{s}, \, r = " + str(REAL_RADIUS_EDITABLE) + r"\, \text{cm}, \, h = " + str(REAL_HEIGHT_EDITABLE) + r"\, \text{cm}",
            font_size=32
        ).to_edge(RIGHT).shift(UP * 3, LEFT * 2)
        self.play(Write(known_values))
        self.wait(1)

        # Write out formula for volume of a cone
        volume_formula = MathTex(r"V = \frac{1}{3} \pi r^2 h", font_size=32).next_to(known_values, DOWN, buff=0.25)
        self.play(Write(volume_formula))
        self.wait(1)

        similar_triangles_text = Text("Using similar triangles: ", font_size=24).next_to(volume_formula, DOWN, buff=0.25)
        similar_triangles = MathTex(r"\frac{r}{" + str(REAL_RADIUS_EDITABLE) + r"} = \frac{h}{" + str(REAL_HEIGHT_EDITABLE) + r"}", font_size=32).next_to(similar_triangles_text, DOWN, buff=0.25)

        triangle_1_points = [cone.get_top(), cone.get_bottom(), cone.get_top() + RIGHT * cone_radius]
        triangle_2_points = [cone.get_bottom(), cone.get_top() + DOWN * (cone_height /2), cone.get_top() + DOWN * (cone_height / 2) + RIGHT * (cone_radius / 2)]

        triangle_1 = Polygon(*triangle_1_points, stroke_color=GREEN, stroke_width=2, fill_color=GREEN ,fill_opacity=0.3)
        triangle_2 = Polygon(*triangle_2_points, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.3)

        similar_triangles_radius_label = MathTex(str(REAL_RADIUS_EDITABLE), font_size=24).next_to((triangle_1_points[0] + triangle_1_points[2])/2, UP)
        similar_triangles_r_label = MathTex("r", font_size=24).next_to((triangle_2_points[1] + triangle_2_points[2])/2, UP)

        similar_triangles_half_height_line = Line(cone.get_bottom() + RIGHT * cone_radius, cone.get_top() + DOWN * (cone_height / 2) + RIGHT * cone_radius, color=YELLOW)
        similar_triangles_full_height_line = Line(cone.get_bottom() + RIGHT * (cone_radius + 0.3), cone.get_top() + RIGHT * (cone_radius + 0.3), color=YELLOW)

        similar_triangles_half_height_label = MathTex("h", font_size=24).next_to(similar_triangles_half_height_line, RIGHT, buff=0.1)
        similar_triangles_full_height_label = MathTex(str(REAL_HEIGHT_EDITABLE), font_size=24).next_to(similar_triangles_full_height_line, RIGHT, buff=0.1)


        self.play(Create(triangle_1), Create(triangle_2), Write(similar_triangles_text), Write(similar_triangles))
        self.wait(1)

        self.play(Write(similar_triangles_radius_label), Write(similar_triangles_r_label), Write(similar_triangles_half_height_line), Write(similar_triangles_full_height_line), Write(similar_triangles_half_height_label), Write(similar_triangles_full_height_label))
        self.wait(1)

        # Show multiplication of 8 on both sides
        solve_for_r_text = Text("Solving for r:", font_size=24).next_to(similar_triangles, DOWN, buff=0.25)
        solve_for_r = MathTex(r"r = \frac{" + str(REAL_RADIUS_EDITABLE) + r"h}{" + str(REAL_HEIGHT_EDITABLE) + r"}", font_size=32).next_to(solve_for_r_text, DOWN, buff=0.25)
        

        self.play(Write(solve_for_r_text), Write(solve_for_r))
        self.wait(1)

        # Fade out the previous explanation and equation
        self.play(FadeOut(similar_triangles_text), FadeOut(solve_for_r_text), FadeOut(similar_triangles), FadeOut(triangle_1), FadeOut(triangle_2), FadeOut(similar_triangles_radius_label), FadeOut(similar_triangles_r_label), FadeOut(similar_triangles_half_height_line), FadeOut(similar_triangles_full_height_line), FadeOut(similar_triangles_half_height_label), FadeOut(similar_triangles_full_height_label))

        # Move the new equation (after multiplying by 8) up under the volume formula
        self.play(solve_for_r.animate.next_to(volume_formula, DOWN, buff=0.25))

        self.wait(1)

        simplify_text = Text("Simplify the expression:", font_size=24).next_to(solve_for_r, DOWN, buff=0.25)
        
        gcd_value = gcd(REAL_RADIUS_EDITABLE, REAL_HEIGHT_EDITABLE)
        simplified_num = REAL_RADIUS_EDITABLE // gcd_value
        simplified_denom = REAL_HEIGHT_EDITABLE // gcd_value
        
        simplified_exp = MathTex(r"r = \frac{" + str(simplified_num) + r"h}{" + str(simplified_denom) + r"}", font_size=32).next_to(simplify_text, DOWN, buff=0.25)

        self.play(Write(simplify_text), Write(simplified_exp))
        self.wait(1)

        self.play(FadeOut(simplify_text), FadeOut(solve_for_r))
        self.play(simplified_exp.animate.next_to(volume_formula, DOWN, buff=0.25))
        self.wait(1)


        # Substitute r = 2h/5 into the volume formula (transform in place)
        substituted_volume_formula = MathTex(r"V = \frac{1}{3} \pi \left(\frac{" + str(simplified_num) + r"h}{" + str(simplified_denom) + r"}\right)^2 h", font_size=32)
        substituted_volume_formula.move_to(volume_formula.get_center())  # Keep it in the same place as the original formula

        self.play(Transform(volume_formula, substituted_volume_formula))
        self.play(FadeOut(simplified_exp))
        self.wait(1)

        #Expand (2h/5)^2 to 4h^2/25
        squared_num = simplified_num**2
        squared_denom = simplified_denom**2

        expanded_formula = MathTex(r"V = \frac{1}{3} \pi \cdot \frac{" + str(squared_num) + r"h^2}{" + str(squared_denom) + r"} \cdot h", font_size=32)
        expanded_formula.move_to(volume_formula.get_center())  # Keep in the same place
        self.play(Transform(volume_formula, expanded_formula))
        self.wait(2)

        #Combine h terms to get (1/3)(pi)(4/25)h^3
        combined_h_terms_formula = MathTex(r"V = \frac{1}{3} \pi \cdot \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} h^3", font_size=32)
        combined_h_terms_formula.move_to(volume_formula.get_center())  # Keep in the same place
        self.play(Transform(volume_formula, combined_h_terms_formula))
        self.wait(2)

        #Combine the fractions to simplify to (4pi/75)h^3
        """ combined_denom = squared_denom * 3
        simplified_volume_formula = MathTex(r"V = \frac{" + str(squared_num) + r"\pi}{" + str(combined_denom) + r"} h^3", font_size=32)
        simplified_volume_formula.move_to(volume_formula.get_center())  # Keep in the same place
        self.play(Transform(volume_formula, simplified_volume_formula))
        self.wait(2) """

        # Add text for taking the derivative
        derivative_text = Text("Take the derivative on both sides:", font_size=24).next_to(combined_h_terms_formula, DOWN, buff=0.25)
        self.play(Write(derivative_text))
        self.wait(1)

        # Show the derivative being applied to both sides of the formula
        derivative_formula = MathTex(r"\frac{d}{dt} \left( V \right) = \frac{d}{dt} \left( \frac{1}{3} \pi \cdot \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} h^3 \right)", font_size=32).next_to(derivative_text, DOWN, buff=0.25)
        self.play(Write(derivative_formula))
        self.wait(1)

        # Differentiate terms in place
        left_side_transformation = MathTex(r"\frac{dV}{dt} = \frac{1}{3} \pi \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} \cdot \frac{d}{dt} \left( h^3 \right)", font_size=32).move_to(derivative_formula)

        self.play(Transform(derivative_formula, left_side_transformation))
        self.wait(1)

        # Add text for using the chain rule
        chain_rule_text = Text("Using the chain rule:", font_size=24).next_to(left_side_transformation, DOWN, buff=0.25)
        self.play(Write(chain_rule_text))
        self.wait(1)

        # Apply the chain rule for the right side and differentiate h^3
        chain_rule_equation = MathTex(r"\frac{dV}{dt} = \frac{1}{3} \pi \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} \cdot 3h^2 \frac{dh}{dt}", font_size=32).next_to(chain_rule_text, DOWN, buff=0.25)

        # Show the transformation to the new equation with the chain rule applied
        self.play(Write(chain_rule_equation))
        self.wait(1)

        # Perform in-place transformation, combining the constants 4/75 and 3
        simplify_constants_1 = MathTex(r"\frac{dV}{dt} = 3 \cdot \frac{1}{3} \pi \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} h^2 \frac{dh}{dt}", font_size=32).move_to(chain_rule_equation)
        simplify_constants = MathTex(r"\frac{dV}{dt} = \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} \pi h^2 \frac{dh}{dt}", font_size=32).move_to(chain_rule_equation)

        # Animate the transformation in place
        self.play(Transform(chain_rule_equation, simplify_constants_1))
        self.wait(2)
        self.play(Transform(chain_rule_equation, simplify_constants))
        self.wait(2)

        # Perform in-place transformation, simplifying 12/75 to 4/25
        """ simplify_fraction = MathTex(r"\frac{dV}{dt} = \frac{4\pi}{25} h^2 \frac{dh}{dt}", font_size=32).move_to(simplify_constants)

        # Animate the transformation in place
        self.play(Transform(chain_rule_equation, simplify_fraction))
        self.wait(1) """

        # Text indicating the value of h at halfway down the cone
        halfway_text = Text("Halfway down the cone, h = " + str(REAL_HEIGHT_EDITABLE/2), font_size=24).next_to(simplify_constants, DOWN, buff=0.25)

        # Equation with values plugged in (-15 for dV/dt and 10 for h)
        plugged_in_values = MathTex(r"-" + str(VOLUME_LOSS_EDITABLE) + r" = \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} \pi (" + str(REAL_HEIGHT_EDITABLE/2) +r")^2 \frac{dh}{dt}", font_size=32).next_to(halfway_text, DOWN, buff=0.25)

        # Animate writing the text and the equation
        self.play(Write(halfway_text))
        self.play(Write(plugged_in_values))
        self.wait(1)

        # Solve for dh/dt
        # Step 1: Transform 10^2 into 100
        half_height_squared = (REAL_HEIGHT_EDITABLE / 2)**2
        step_1 =  MathTex(r"-" + str(VOLUME_LOSS_EDITABLE) + r" = \frac{" + str(squared_num) + r"}{" + str(squared_denom) + r"} \pi (" + str(half_height_squared) +r") \frac{dh}{dt}", font_size=32).move_to(plugged_in_values)
        self.play(Transform(plugged_in_values, step_1))
        self.wait(2)

        # Step 2: Multiply the constants (4 * 100) to get 400pi/25
        half_height_times_num = half_height_squared * squared_num
        step_2 = MathTex(r"-" + str(VOLUME_LOSS_EDITABLE) + r" = \frac{" + str(half_height_times_num) + r"\pi}{" + str(squared_denom) + r"} \frac{dh}{dt}", font_size=32).move_to(step_1)
        self.play(Transform(plugged_in_values, step_2))
        self.wait(2)

        """  # Step 3: Simplify 400pi/25 to 16pi
        step_3 = MathTex(r"-15 = 16\pi \frac{dh}{dt}", font_size=32).move_to(step_2)
        self.play(Transform(plugged_in_values, step_3))
        self.wait(2) """

        # Step 4: Divide 16pi over to solve for dh/dt
        volume_loss_times_denom = VOLUME_LOSS_EDITABLE * squared_denom
        step_4 = MathTex(r"\frac{-" + str(volume_loss_times_denom) +r"}{" + str(half_height_times_num) + r"\pi} = \frac{dh}{dt}", font_size=32).move_to(step_2)
        self.play(Transform(plugged_in_values, step_4))
        self.wait(2)

        # Final expression for dh/dt
        final_gcd = gcd(int(volume_loss_times_denom), int(half_height_times_num))
        final_num = volume_loss_times_denom / final_gcd
        final_denom = half_height_times_num / final_gcd
        final_solution = MathTex(r"\frac{dh}{dt} = \frac{-" +str(final_num) + r"}{" + str(final_denom) + r"\pi} \, \text{cm/s}", font_size=32).next_to(step_4, DOWN, buff=0.75)

        # Create a yellow rectangle around the final solution
        rect = SurroundingRectangle(final_solution, color=YELLOW)

        # Display the final solution and the rectangle
        self.play(Write(final_solution))
        self.play(Create(rect))
        self.wait(1)


class FadeTransformSubmobjects(Scene):
    def construct(self):
        SHAPE1_COLOR_EDITABLE = RED
        SHAPE2_COLOR_EDITABLE = BLUE
        SHAPE3_COLOR_EDITABLE = GREEN
        SHAPE4_COLOR_EDITABLE = YELLOW
        SHAPE1_OPACITY_EDITABLE = 1
        SHAPE2_OPACITY_EDITABLE = 0.5
        SHAPE3_OPACITY_EDITABLE = 0.25
        SHAPE4_OPACITY_EDITABLE = 0
        
        
        src = VGroup(
            Square(
                color=SHAPE1_COLOR_EDITABLE, 
                fill_opacity=SHAPE1_OPACITY_EDITABLE
            ), 
            Circle(
                color=SHAPE2_COLOR_EDITABLE, 
                fill_opacity=SHAPE2_OPACITY_EDITABLE
            ).shift(LEFT + UP)
        ).shift(LEFT)
        
        target = VGroup(
            Circle(
                color=SHAPE3_COLOR_EDITABLE, 
                fill_opacity=SHAPE3_OPACITY_EDITABLE
            ), 
            Triangle(
                color=SHAPE4_COLOR_EDITABLE, 
                fill_opacity=SHAPE4_OPACITY_EDITABLE
            ).shift(RIGHT + DOWN)
        ).shift(RIGHT)
        
        
        self.play(FadeIn(src))
        self.play(
            FadeTransform(src, target),
        )
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])