from geometry_utils import *
import numpy as np

class ArcPath():
    def __init__(self, gcode_writer=None, center=[0,0], z=0, pz=0, r=1, f=100, pf=30, spindle_speed=1000, bit_width=0, direction="cw", start_point=[0,0], end_point=[0,0], repeats=0):
        self.gw = gcode_writer
        self.center = np.array(center)
        self.travel_z = z
        self.cut_depth = pz
        self.bit_width = bit_width # cuts are made offset so that we only cut the specified radius from center
        self.radius = r-bit_width/2 # radius of circle
        self.f = f # feedrate
        self.plunge_feedrate = pf
        self.spindle_speed = spindle_speed
        self.direction = direction # directions can be cw: clockwise or ccw: counter-clockwise
        self.repeats = repeats
        self.start_point = np.array([0,0])
        self.end_point = np.array([0,0])
        self.set_start_end_points(start_point, end_point)
    def cut_arc(self):
        goto_plunge(gw=self.gw, x=self.start_point[0], y=self.start_point[1], z=self.travel_z, zpd=self.cut_depth)
        # repeat cut arc path
        for iteration in range(0,self.repeats + 1): # repeats start after the first
            # then cut the arc out
            self.gw.arc_path(center=self.center, radius=self.radius, start_point=self.start_point, end_point=self.end_point, direction=self.direction, feedrate=self.f)
    def set_start_end_points(self, start_point, end_point):
        # assumed that the points will be on the circle
        assert(dist_between_two_points(self.center, start_point) == self.radius and
               dist_between_two_points(self.center, end_point) == self.radius)
        self.start_point = start_point
        self.end_point = end_point

class CirclePath(ArcPath):
    def set_start_end_points(self, start_point, end_point):
        # in a circle set the start and end points to the same point on the circle
        self.start_point = np.array([self.center[0] + self.radius, self.center[1]])
        self.end_point = self.start_point

def goto_plunge(gw=None, x=None, y=None, z=None, zpd=0, pf=10, s=10000):
    # first go to start_point
    gw.goto(x=x, y=y, z=z)
    # then plunge the z
    gw.set_spindle_speed(s)
    gw.goto(z=zpd, f=pf)
