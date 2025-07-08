from manim import *

class FullSolution(Scene):
    def construct(self):
        
        title1 = Text("Calculate the Volume of the Cylinder", font_size=36)
        self.play(Write(title1))
        self.wait(0.5)
        body1 = Text("The volume of a cylinder can be calculated using the formula V = pi * r^2 * h. Here, r is the radius (4 meters) and h is the height (10 meters).", font_size=24).next_to(title1, DOWN)
        self.play(Write(body1))
        self.wait(1)
        
        cue_obj = Text("Show the formula for the volume of a cylinder with labeled dimensions.", font_size=28, color=YELLOW).to_edge(DOWN)
        
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
        
        title3 = Text("Calculate the Volume", font_size=36)
        self.play(Write(title3))
        self.wait(0.5)
        body3 = Text("Now, calculate the volume: V = pi * 160. Using approximately 3.14 for pi, we find V is about 502.4 cubic meters.", font_size=24).next_to(title3, DOWN)
        self.play(Write(body3))
        self.wait(1)
        
        cue_obj = Text("Animate the calculation of volume using pi.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title3), FadeOut(body3))
        self.wait(0.5)
        
        title4 = Text("Convert Volume to Liters", font_size=36)
        self.play(Write(title4))
        self.wait(0.5)
        body4 = Text("Since 1 cubic meter equals 1000 liters, convert the volume from cubic meters to liters: 502.4 cubic meters * 1000 liters/cubic meter equals 502400 liters.", font_size=24).next_to(title4, DOWN)
        self.play(Write(body4))
        self.wait(1)
        
        cue_obj = Text("Show the conversion from cubic meters to liters.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title4), FadeOut(body4))
        self.wait(0.5)
        
        title5 = Text("Determine Fill Rate", font_size=36)
        self.play(Write(title5))
        self.wait(0.5)
        body5 = Text("The tank is being filled at a rate of 20 liters per second. To find the time taken to fill the tank, we will divide the total volume in liters by the fill rate.", font_size=24).next_to(title5, DOWN)
        self.play(Write(body5))
        self.wait(1)
        
        cue_obj = Text("Illustrate the division of total volume by fill rate.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title5), FadeOut(body5))
        self.wait(0.5)
        
        title6 = Text("Calculate Time to Fill the Tank", font_size=36)
        self.play(Write(title6))
        self.wait(0.5)
        body6 = Text("Now, calculate the time: Time = 502400 liters / 20 liters/second. This gives a total time of 25120 seconds.", font_size=24).next_to(title6, DOWN)
        self.play(Write(body6))
        self.wait(1)
        
        cue_obj = Text("Show the calculation of time taken to fill the tank.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title6), FadeOut(body6))
        self.wait(0.5)
        
        title7 = Text("Convert Time to Hours", font_size=36)
        self.play(Write(title7))
        self.wait(0.5)
        body7 = Text("To make the time more understandable, convert seconds into hours. There are 3600 seconds in an hour, so divide 25120 seconds by 3600 seconds/hour.", font_size=24).next_to(title7, DOWN)
        self.play(Write(body7))
        self.wait(1)
        
        cue_obj = Text("Visualize the conversion from seconds to hours.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title7), FadeOut(body7))
        self.wait(0.5)
        
        title8 = Text("Final Result", font_size=36)
        self.play(Write(title8))
        self.wait(0.5)
        body8 = Text("The final result shows that it takes approximately 6.97 hours to fill the tank. This can be rounded to about 7 hours for simplicity.", font_size=24).next_to(title8, DOWN)
        self.play(Write(body8))
        self.wait(1)
        
        cue_obj = Text("Display the final time result clearly.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title8), FadeOut(body8))
        self.wait(0.5)
        
