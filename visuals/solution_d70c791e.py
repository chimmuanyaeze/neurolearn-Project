from manim import *

class FullSolution(Scene):
    def construct(self):
        
        title1 = Text("Calculate the Volume of the Cylinder", font_size=36)
        self.play(Write(title1))
        self.wait(0.5)
        body1 = Text("The volume of a cylinder can be calculated using the formula V = pi * r^2 * h, where r is the radius and h is the height. For this tank, we will substitute r = 4 meters and h = 10 meters into the formula.", font_size=24).next_to(title1, DOWN)
        self.play(Write(body1))
        self.wait(1)
        
        cue_obj = Text("Show the formula for the volume of a cylinder with labeled dimensions.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title1), FadeOut(body1))
        self.wait(0.5)
        
        title2 = Text("Substitute Values into the Volume Formula", font_size=36)
        self.play(Write(title2))
        self.wait(0.5)
        body2 = Text("Substituting the values into the formula gives us V = pi * (4^2) * 10. This simplifies to V = pi * 16 * 10.", font_size=24).next_to(title2, DOWN)
        self.play(Write(body2))
        self.wait(1)
        
        cue_obj = Text("Highlight the substitution of values into the formula.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title2), FadeOut(body2))
        self.wait(0.5)
        
        title3 = Text("Calculate the Volume in Cubic Meters", font_size=36)
        self.play(Write(title3))
        self.wait(0.5)
        body3 = Text("Now, calculate the volume: V = pi * 160. Using an approximate value of pi (3.14), we find V ≈ 502.4 cubic meters. This is the volume in cubic meters.", font_size=24).next_to(title3, DOWN)
        self.play(Write(body3))
        self.wait(1)
        
        cue_obj = Text("Show the calculation of volume with pi approximated.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title3), FadeOut(body3))
        self.wait(0.5)
        
        title4 = Text("Convert Volume to Liters", font_size=36)
        self.play(Write(title4))
        self.wait(0.5)
        body4 = Text("Since 1 cubic meter is equal to 1000 liters, we convert the volume from cubic meters to liters. Therefore, 502.4 cubic meters is equal to 502400 liters.", font_size=24).next_to(title4, DOWN)
        self.play(Write(body4))
        self.wait(1)
        
        cue_obj = Text("Illustrate the conversion from cubic meters to liters.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title4), FadeOut(body4))
        self.wait(0.5)
        
        title5 = Text("Determine the Filling Rate", font_size=36)
        self.play(Write(title5))
        self.wait(0.5)
        body5 = Text("The pump fills the tank at a rate of 20 liters per second. To find out how long it will take to fill the tank, we need to divide the total volume by the filling rate.", font_size=24).next_to(title5, DOWN)
        self.play(Write(body5))
        self.wait(1)
        
        cue_obj = Text("Show the filling rate and total volume side by side.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title5), FadeOut(body5))
        self.wait(0.5)
        
        title6 = Text("Calculate Time to Fill the Tank", font_size=36)
        self.play(Write(title6))
        self.wait(0.5)
        body6 = Text("To find the time in seconds, we calculate time = total volume / filling rate. This gives us time = 502400 liters / 20 liters per second, which equals 25120 seconds.", font_size=24).next_to(title6, DOWN)
        self.play(Write(body6))
        self.wait(1)
        
        cue_obj = Text("Display the division of total volume by filling rate.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title6), FadeOut(body6))
        self.wait(0.5)
        
        title7 = Text("Convert Time to Minutes", font_size=36)
        self.play(Write(title7))
        self.wait(0.5)
        body7 = Text("Since we want the time in minutes, we convert seconds to minutes by dividing by 60. Therefore, 25120 seconds is approximately 418.67 minutes.", font_size=24).next_to(title7, DOWN)
        self.play(Write(body7))
        self.wait(1)
        
        cue_obj = Text("Illustrate the conversion from seconds to minutes.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title7), FadeOut(body7))
        self.wait(0.5)
        
        title8 = Text("Summarize Results", font_size=36)
        self.play(Write(title8))
        self.wait(0.5)
        body8 = Text("The total volume of the tank is 502400 liters, and it will take approximately 418.67 minutes to fill the tank completely. This gives a clear understanding of the tank's capacity and filling time.", font_size=24).next_to(title8, DOWN)
        self.play(Write(body8))
        self.wait(1)
        
        cue_obj = Text("Show a summary of the final results.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title8), FadeOut(body8))
        self.wait(0.5)
        
