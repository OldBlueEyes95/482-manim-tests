from manim import *

# Set the resolution and frame size
config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 10.0
config.frame_width = 18.0
config.media_width = "100%"

class RelatedRatesAnimation(Scene):
    def construct(self):
        # Step 1: Create a circle and animate its growth
        circle = Circle(radius=1, color=BLUE).shift(LEFT * 4)  # Move the circle slightly to the right
        radius_line = Line(circle.get_center(), circle.get_right(), color=YELLOW)
        self.play(Create(circle), Create(radius_line))
        
        # Step 2: Create number lines for radius and area
        radius_number_line = NumberLine(x_range=[0, 5, 1], length=5, include_numbers=True).shift(RIGHT * 4.5 + UP * 2.5)
        area_number_line = NumberLine(x_range=[0, 80, 10], length=5, include_numbers=True).shift(RIGHT * 4.5 + UP)

        radius_label = MathTex("r").next_to(radius_number_line, UP)
        area_label = MathTex("A").next_to(area_number_line, UP)

        original_radius_text = MathTex("Original \, Radius = 1 \, \mathrm{unit}").scale(0.7).next_to(area_number_line, DOWN, buff=0.5)

        self.play(Create(radius_number_line), Create(area_number_line), Write(radius_label), Write(area_label), Write(original_radius_text))
        
        # Step 3: Create ValueTrackers for radius and area
        radius_tracker = ValueTracker(1)
        area_tracker = ValueTracker(PI * radius_tracker.get_value()**2)
        
        # Step 4: Create dots for radius and area
        radius_dot = Dot(radius_number_line.n2p(radius_tracker.get_value()), color=YELLOW)
        area_dot = Dot(area_number_line.n2p(area_tracker.get_value()), color=YELLOW)
        
        self.play(Create(radius_dot), Create(area_dot))

        radius_value_text = DecimalNumber(radius_tracker.get_value(), num_decimal_places=2).next_to(radius_number_line, RIGHT)
        area_value_text = DecimalNumber(area_tracker.get_value(), num_decimal_places=2).next_to(area_number_line, RIGHT)

        self.add(radius_value_text, area_value_text)
        
        # Step 5: Update functions for the dots and circle
        def update_circle(mob):
            new_radius = radius_tracker.get_value()
            new_circle = Circle(radius=new_radius, color=BLUE).shift(LEFT * 4)
            mob.become(new_circle)
        
        def update_radius_line(mob):
            new_radius = radius_tracker.get_value()
            new_radius_line = Line(circle.get_center(), circle.get_center() + RIGHT * new_radius, color=YELLOW)
            mob.become(new_radius_line)
        
        def update_radius_dot(mob):
            mob.move_to(radius_number_line.n2p(radius_tracker.get_value()))
        
        def update_area_dot(mob):
            new_area = PI * radius_tracker.get_value()**2
            area_tracker.set_value(new_area)
            mob.move_to(area_number_line.n2p(area_tracker.get_value()))

        def update_radius_text(mob):
            mob.set_value(radius_tracker.get_value())
        
        def update_area_text(mob):
            mob.set_value(area_tracker.get_value())
        
        circle.add_updater(update_circle)
        radius_line.add_updater(update_radius_line)
        radius_dot.add_updater(update_radius_dot)
        area_dot.add_updater(update_area_dot)
        radius_value_text.add_updater(update_radius_text)
        area_value_text.add_updater(update_area_text)

        self.wait(2)
        
        # Step 6: Animate the radius growth
        self.play(radius_tracker.animate.set_value(4), run_time=8, rate_func=linear)
        
        # Step 7: Remove updaters and wait
        circle.remove_updater(update_circle)
        radius_line.remove_updater(update_radius_line)
        radius_dot.remove_updater(update_radius_dot)
        area_dot.remove_updater(update_area_dot)
        
        self.wait(2)
        
        # Step 8: Add text to explain the rate of change of the area
        
        rate_of_change_radius_text = MathTex("Rate \, of \, Change \, of \, Radius = \\frac{3}{8} \, \mathrm{unit/s}").scale(0.7).next_to(original_radius_text, DOWN)
        differentiation_text = MathTex("Area = \\pi r^2").scale(0.7).next_to(rate_of_change_radius_text, DOWN)
        differentiation_step_text = MathTex("Rate \, of \, Change \, of \, Area = 2\\pi r \\frac{dr}{dt} \, \mathrm{unit^2/s}").scale(0.7).next_to(differentiation_text, DOWN)
        calculation_text = MathTex("Rate \, of \, Change \, of \, Area = 2\\pi (1) \\left(\\frac{3}{8}\\right) \, \mathrm{unit^2/s}").scale(0.7).next_to(differentiation_step_text, DOWN)
        result_text = MathTex("Rate \, of \, Change \, of \, Area = \\frac{3\\pi}{4} \, \mathrm{unit^2/s}").scale(0.7).next_to(calculation_text, DOWN)
        
        self.play(Write(rate_of_change_radius_text))
        self.play(Write(differentiation_text))
        self.play(Write(differentiation_step_text))
        self.play(Write(calculation_text))
        self.play(Write(result_text))
        
        self.wait(2)

if __name__ == "__main__":
    scene = RelatedRatesAnimation()
    scene.render()