from manim import *

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


class WasherMethod(MyThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        axes_range = [-5, 5, 1]
        standing_axes = ThreeDAxes(
            x_range=axes_range, y_range=axes_range, z_range=axes_range
        ).move_to(ORIGIN)
        # we lie about the axes: internally y is depth and z is height, but the student expects y as height and z as depth
        # axes_labels = standing_axes.get_axis_labels(
        #     Text("x-axis").scale(0.7), Text("z-axis").scale(0.45), Text("y-axis").scale(0.45)
        # )
        
        self.add(standing_axes)
        
        #TODO stretch goal: add a flat side image of the function in 2D space
        
        # Curve and Surface Config
        t_range = [0, 5]
        u_range = t_range
        v_range = [0, 2 * PI]
        resolution = (20, 40)
        fill_opacity = 0.7
        formula_font_size = 28
        
        # Linear function
        '''
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
        '''
        
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
        # e_cubic_rstrs =  [r"V",  r"=", r"\pi", r"\int_a^b",    r"[x^3]^2", r"dx"]
        # e_cubic_colors = [BLUE, WHITE,    RED,       GREEN,      YELLOW, GREEN]
        # e_cubic = MathTex(*e_cubic_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        # make_fixed(e_cubic)
        # apply_colors(e_cubic, e_cubic_colors)
        
        # e_cubic_final_rstrs =  [r"V",  r"=", r"\pi", r"\frac{1}{7} x^7"]
        # e_cubic_final_colors = [BLUE, WHITE,    RED,            GREEN_C]
        # e_cubic_final = MathTex(*e_cubic_final_rstrs, font_size=formula_font_size).to_corner(UR, buff=0.5)
        # make_fixed(e_cubic_final)
        # apply_colors(e_cubic_final, e_cubic_final_colors)
        
        
        '''
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
        '''
        
        # cubic
        self.play(Write(f_cubic))
        self.play(
            Rotate(f_cubic, -2*PI, about_point=standing_axes.get_origin(), axis=X_AXIS),
            Write(s_cubic, rate_func=rate_functions.linear)
        )
        self.wait(1)
        self.play(FadeOut(f_cubic, s_cubic))