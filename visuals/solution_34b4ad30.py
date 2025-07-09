from manim import *

class FullSolution(Scene):
    def construct(self):
        
        title1 = Text("Calculate the Volume of the Cylinder", font_size=36)
        self.play(Write(title1))
        self.wait(0.5)
        body1 = Text("The volume of a cylinder can be calculated using the formula V = pi * r^2 * h, where r is the radius and h is the height. For this tank, we will substitute r = 4 meters and h = 10 meters into the formula.", font_size=24).next_to(title1, DOWN)
        self.play(Write(body1))
        self.wait(1)
        
        cue_obj = Text("Show the formula for the volume of a cylinder with labeled radius and height.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title1), FadeOut(body1))
        self.wait(0.5)
        
        title2 = Text("Substitute Values into the Formula", font_size=36)
        self.play(Write(title2))
        self.wait(0.5)
        body2 = Text("Now, we substitute the values into the formula: V = pi * (4^2) * 10. This simplifies to V = pi * 16 * 10.", font_size=24).next_to(title2, DOWN)
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
        body3 = Text("Next, we calculate the volume: V = 160 * pi cubic meters. Using an approximate value for pi (3.14), we find V is about 502.4 cubic meters.", font_size=24).next_to(title3, DOWN)
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
        body4 = Text("Since 1 cubic meter is equal to 1000 liters, we convert the volume from cubic meters to liters. Therefore, 502.4 cubic meters is equal to 502400 liters.", font_size=24).next_to(title4, DOWN)
        self.play(Write(body4))
        self.wait(1)
        
        cue_obj = Text("Show the conversion from cubic meters to liters.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title4), FadeOut(body4))
        self.wait(0.5)
        
        title5 = Text("Determine Fill Rate in Liters per Second", font_size=36)
        self.play(Write(title5))
        self.wait(0.5)
        body5 = Text("The pump fills the tank at a rate of 20 liters per second. We need to find out how many seconds it will take to fill the entire tank of 502400 liters.", font_size=24).next_to(title5, DOWN)
        self.play(Write(body5))
        self.wait(1)
        
        cue_obj = Text("Illustrate the fill rate of the pump.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title5), FadeOut(body5))
        self.wait(0.5)
        
        title6 = Text("Calculate Time to Fill the Tank", font_size=36)
        self.play(Write(title6))
        self.wait(0.5)
        body6 = Text("To find the time in seconds, we divide the total volume by the fill rate: time = 502400 liters / 20 liters/second. This gives us a total time of 25120 seconds.", font_size=24).next_to(title6, DOWN)
        self.play(Write(body6))
        self.wait(1)
        
        cue_obj = Text("Show the division of total volume by fill rate.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title6), FadeOut(body6))
        self.wait(0.5)
        
        title7 = Text("Convert Time to Minutes", font_size=36)
        self.play(Write(title7))
        self.wait(0.5)
        body7 = Text("Finally, to convert seconds into minutes, we divide the total seconds by 60. Thus, 25120 seconds is approximately 418.67 minutes.", font_size=24).next_to(title7, DOWN)
        self.play(Write(body7))
        self.wait(1)
        
        cue_obj = Text("Visualize the conversion from seconds to minutes.", font_size=28, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        
        self.play(FadeOut(title7), FadeOut(body7))
        self.wait(0.5)
        
