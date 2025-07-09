from manim import *

class FullSolution(Scene):
    def construct(self):
        
        title1 = Text("Calculate the Volume of the Cylinder", font_size=36)
        self.play(Write(title1))
        self.wait(0.5)
        body1 = Text("To find the volume of a cylinder, use the formula V = pi * r^2 * h. Here, r is the radius (4 meters) and h is the height (10 meters).", font_size=24).next_to(title1, DOWN)
        self.play(Write(body1))
        self.wait(1)
        
        cue_obj = Text("Show the formula for the volume of a cylinder.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title1), FadeOut(body1))
        self.wait(0.5)
        
        title2 = Text("Substitute Values into the Formula", font_size=36)
        self.play(Write(title2))
        self.wait(0.5)
        body2 = Text("Substituting the values into the formula gives V = pi * (4^2) * 10. This simplifies to V = pi * 16 * 10.", font_size=24).next_to(title2, DOWN)
        self.play(Write(body2))
        self.wait(1)
        
        cue_obj = Text("Highlight the substitution of values into the volume formula.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title2), FadeOut(body2))
        self.wait(0.5)
        
        title3 = Text("Calculate the Volume in Cubic Meters", font_size=36)
        self.play(Write(title3))
        self.wait(0.5)
        body3 = Text("Now, calculate the volume: V = pi * 160. Using an approximate value of pi (3.14), the volume is about 502.4 cubic meters.", font_size=24).next_to(title3, DOWN)
        self.play(Write(body3))
        self.wait(1)
        
        cue_obj = Text("Display the calculation of volume using pi.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title3), FadeOut(body3))
        self.wait(0.5)
        
        title4 = Text("Convert Volume to Liters", font_size=36)
        self.play(Write(title4))
        self.wait(0.5)
        body4 = Text("Since 1 cubic meter equals 1000 liters, multiply the volume in cubic meters by 1000. Thus, 502.4 cubic meters equals 502400 liters.", font_size=24).next_to(title4, DOWN)
        self.play(Write(body4))
        self.wait(1)
        
        cue_obj = Text("Illustrate the conversion from cubic meters to liters.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title4), FadeOut(body4))
        self.wait(0.5)
        
        title5 = Text("Determine Filling Time in Seconds", font_size=36)
        self.play(Write(title5))
        self.wait(0.5)
        body5 = Text("To find out how long it takes to fill the tank, divide the total volume by the filling rate. So, 502400 liters divided by 20 liters per second equals 25120 seconds.", font_size=24).next_to(title5, DOWN)
        self.play(Write(body5))
        self.wait(1)
        
        cue_obj = Text("Show the division of total volume by filling rate.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title5), FadeOut(body5))
        self.wait(0.5)
        
        title6 = Text("Convert Time to Minutes", font_size=36)
        self.play(Write(title6))
        self.wait(0.5)
        body6 = Text("Now, convert the time from seconds to minutes by dividing by 60. Therefore, 25120 seconds divided by 60 equals approximately 418.67 minutes.", font_size=24).next_to(title6, DOWN)
        self.play(Write(body6))
        self.wait(1)
        
        cue_obj = Text("Visualize the conversion from seconds to minutes.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title6), FadeOut(body6))
        self.wait(0.5)
        
        title7 = Text("Summarize the Results", font_size=36)
        self.play(Write(title7))
        self.wait(0.5)
        body7 = Text("The total volume of the tank is 502400 liters, and it will take about 418.67 minutes to fill the tank completely at the given rate.", font_size=24).next_to(title7, DOWN)
        self.play(Write(body7))
        self.wait(1)
        
        cue_obj = Text("Display the final results clearly.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title7), FadeOut(body7))
        self.wait(0.5)
        
