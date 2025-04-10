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


class CylindricalShells(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        standing_axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1]
        ).move_to(ORIGIN)
        axes_labels = standing_axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
        
        self.add(standing_axes, axes_labels)
        
        # Define 3D parametric curves (x, y, z) where z is the function value
        x_offset = 0
        y_offset = 0 # keep at 0 to align to axis
        z_offset = 0 # keep at 0 to align to axis
        t_range = [0, 5]
        
        f_const = ParametricFunction(
            lambda t: np.array([t + x_offset, y_offset, 1 + z_offset]),  # y=0, z=1 (constant height)
            t_range=t_range, color=RED
        ).set_shade_in_3d(True)
        s_const = Surface(
            lambda u, v: np.array([
                u, 
                1 * np.cos(v),
                1 * np.sin(v)
            ]),
            u_range=[0, 5],
            v_range=[0, 2 * PI],
            resolution=(20, 40),
            checkerboard_colors=[RED, RED_D],
            fill_opacity=0.7
        )
        f__line = ParametricFunction(
            lambda t: np.array([t + x_offset, y_offset, 0.5 * t + z_offset]),  # z = 0.5x
            t_range=t_range, color=BLUE
        ).set_shade_in_3d(True)
        s__line = Surface(
            lambda u, v: np.array([
                u, 
                0.5 * u * np.cos(v),
                0.5 * u * np.sin(v)
            ]),
            u_range=[0, 5],
            v_range=[0, 2 * PI],
            resolution=(20, 40),
            checkerboard_colors=[BLUE, BLUE_D],
            fill_opacity=0.7
        )
        f_cubic = ParametricFunction(
            lambda t: np.array([t + x_offset, y_offset, 0.02 * t**3 + z_offset]),  # z = 0.1x^3
            t_range=t_range, color=GREEN
        ).set_shade_in_3d(True)
        s_cubic = Surface(
            lambda u, v: np.array([
                u, 
                0.02 * u**3 * np.cos(v),
                0.02 * u**3 * np.sin(v)
            ]),
            u_range=[0, 5],
            v_range=[0, 2 * PI],
            resolution=(20, 40),
            checkerboard_colors=[GREEN, GREEN_D],
            fill_opacity=0.7
        )
        
        
        self.play(Write(f_const))
        self.play(
            Rotate(f_const, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s_const, rate_func=rate_functions.linear)
        )
        self.wait(1)
        self.play(FadeOut(f_const, s_const))
        
        self.play(Write(f__line))
        self.play(
            Rotate(f__line, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s__line, rate_func=rate_functions.linear)
        )
        self.wait(1)
        self.play(FadeOut(f__line, s__line))
        
        self.play(Write(f_cubic))
        self.play(
            Rotate(f_cubic, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s_cubic, rate_func=rate_functions.linear)
        )
        self.wait(1)
        self.play(FadeOut(f_cubic, s_cubic))
        
        self.wait(1)