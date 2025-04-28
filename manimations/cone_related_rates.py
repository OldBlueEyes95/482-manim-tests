from manim import *
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
        problem_statement = Tex(*problem_strs, font_size=24).to_edge(UP)
        self.add(problem_statement)
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

if __name__ == "__main__":
    scene = ConeRelatedRates()
    scene.render()
