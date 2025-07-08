from manim import *

class FullSolution(Scene):
    def construct(self):
        
        title1 = Text("Calculate the Volume of the Cylinder", font_size=36)
        self.play(Write(title1))
        self.wait(0.5)
        body1 = Text("The volume of a cylinder is calculated using the formula V = πr²h, where r is the radius and h is the height. Here, we substitute r = 4 meters and h = 10 meters into the formula.", font_size=24).next_to(title1, DOWN)
        self.play(Write(body1))
        self.wait(1)
        
        try:
            cue_obj = MathTex(r"Show the formula V = πr²h with values substituted.", font_size=32, color=YELLOW).to_edge(DOWN)
        except Exception:
            cue_obj = Text("Show the formula V = πr²h with values substituted.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title1), FadeOut(body1))
        self.wait(0.5)
        
        title2 = Text("Substitute Values into the Formula", font_size=36)
        self.play(Write(title2))
        self.wait(0.5)
        body2 = Text("Substituting the values, we get V = π(4)²(10). First, calculate 4², which is 16, then multiply by 10 to get 160. Finally, multiply by π to find the volume.", font_size=24).next_to(title2, DOWN)
        self.play(Write(body2))
        self.wait(1)
        
        cue_obj = Text("Animate the calculation of 4² and then 16 × 10.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title2), FadeOut(body2))
        self.wait(0.5)
        
        title3 = Text("Calculate the Volume in Cubic Meters", font_size=36)
        self.play(Write(title3))
        self.wait(0.5)
        body3 = Text("Now, calculate the volume: V = π × 160. Using π ≈ 3.14, we find V ≈ 502.4 cubic meters. This is the volume in cubic meters.", font_size=24).next_to(title3, DOWN)
        self.play(Write(body3))
        self.wait(1)
        
        cue_obj = Text("Display the multiplication of 160 by π.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title3), FadeOut(body3))
        self.wait(0.5)
        
        title4 = Text("Convert Volume to Liters", font_size=36)
        self.play(Write(title4))
        self.wait(0.5)
        body4 = Text("To convert cubic meters to liters, we use the conversion factor: 1 cubic meter = 1000 liters. Therefore, multiply the volume in cubic meters by 1000 to get the volume in liters.", font_size=24).next_to(title4, DOWN)
        self.play(Write(body4))
        self.wait(1)
        
        cue_obj = Text("Show the conversion from cubic meters to liters (502.4 × 1000).", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title4), FadeOut(body4))
        self.wait(0.5)
        
        title5 = Text("Calculate Total Volume in Liters", font_size=36)
        self.play(Write(title5))
        self.wait(0.5)
        body5 = Text("Calculating 502.4 × 1000 gives us 502400 liters. This is the total volume of water the tank can hold.", font_size=24).next_to(title5, DOWN)
        self.play(Write(body5))
        self.wait(1)
        
        cue_obj = Text("Highlight the final volume of 502400 liters.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title5), FadeOut(body5))
        self.wait(0.5)
        
        title6 = Text("Determine Fill Time in Seconds", font_size=36)
        self.play(Write(title6))
        self.wait(0.5)
        body6 = Text("Next, we need to find out how long it takes to fill the tank at a rate of 20 liters per second. We divide the total volume by the fill rate: 502400 liters ÷ 20 liters/second.", font_size=24).next_to(title6, DOWN)
        self.play(Write(body6))
        self.wait(1)
        
        cue_obj = Text("Show the division of total volume by fill rate.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title6), FadeOut(body6))
        self.wait(0.5)
        
        title7 = Text("Calculate Fill Time in Seconds", font_size=36)
        self.play(Write(title7))
        self.wait(0.5)
        body7 = Text("Performing the division gives us 25120 seconds to fill the tank completely. This is the time in seconds.", font_size=24).next_to(title7, DOWN)
        self.play(Write(body7))
        self.wait(1)
        
        cue_obj = Text("Display the result of the division as 25120 seconds.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title7), FadeOut(body7))
        self.wait(0.5)
        
        title8 = Text("Convert Seconds to Minutes", font_size=36)
        self.play(Write(title8))
        self.wait(0.5)
        body8 = Text("Finally, to convert seconds into minutes, divide the total seconds by 60. So, 25120 seconds ÷ 60 gives us approximately 418.67 minutes.", font_size=24).next_to(title8, DOWN)
        self.play(Write(body8))
        self.wait(1)
        
        cue_obj = Text("Show the conversion from seconds to minutes.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title8), FadeOut(body8))
        self.wait(0.5)
        
