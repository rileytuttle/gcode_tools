import pdb

class GcodeWriter():
    def __init__(self, filename):
        self.filehandle = open(filename, 'w+')
        self.units = "mm"
        self.type = "GRBL"
    def __del__(self):
        self.filehandle.close()
    def write(self, gcode_text):
        self.filehandle.write(f'{gcode_text}\n')
    def comment(self, comment_text):
        self.filehandle.write(f'; {comment_text}\n')
    def block_comment(self, comment_text):
        comment_lines = comment_text.split("\n")
        for line in comment_lines:
            self.comment(line)
    def set_absolute_motion(self):
        self.comment("set to absolute motion")
        self.write("G90")
    def set_units(self, units="mm"):
        if units == "mm":
            self.units = units
            self.comment("setting to mm")
            self.write("G21")
        elif units == "in":
            self.units = units
            self.not_implemented()
        else:
            self.not_implemented()
    def set_spindle_speed(self, speed):
        self.comment(f"spindle to {speed}")
        cmd = f'S{speed}'
        if self.type == "GRBL":
            # not sure why but I have to add an M3 here
            # when sending spindle speed commands
            cmd = f'M3 {cmd}'
        self.write(cmd)
        
    def end_program(self):
        self.comment("end program")
        self.write("M30")
    def goto(self, x=None, y=None, z=None, f=None):
        if x is None and y is None and z is None:
            raise Exception("go nowhere ?")
        if f is None:
            # fast positioning
            # using fast positioning speed
            cmd = "G0"
        else:
            # slower cutting
            cmd = "G1"
        if x:
            cmd = f"{cmd} X{x}"
        if y:
            cmd = f"{cmd} Y{y}"
        if z:
            cmd = f"{cmd} Z{z}"
        if f:
            cmd = f"{cmd} F{f}"
        self.write(cmd)
    def goto_plunge(self, x=None, y=None, z=None, zpd=0, pf=10, s=10000):
        # first go to start_point
        self.goto(x=x, y=y, z=z)
        # then plunge the z
        self.set_spindle_speed(s)
        self.goto(z=zpd, f=pf)
    def arc_path(self, center=[0,0], radius=1, start_point=[0,0], end_point=[0,0], direction="cw", feedrate=100):
        self.comment(f"tracing arc path of {radius}{self.units} from {start_point} to {end_point} with center {center}") 
        if direction == "cw":
            cmd = "G02"
        elif direction == "ccw":
            cmd = "G03"
        else:
            raise ValueError(f"{direction} is not a supported direction")
        # run G02 Xxx Yyy Iii Jjj Ffff
        #   that will do a cw cut in starting at current and ending at
        #   [xx,yy] the center is [current_x - ii, current_y - jj]
        #   with feedrate fff
        ij_offset = center - start_point
        cmd = f"{cmd} X{end_point[0]} Y{end_point[1]} I{ij_offset[0]} J{ij_offset[1]} F{feedrate}"
        self.write(cmd)

    def cut_arc(self, params):
        self.goto_plunge(x=params.start_point[0], y=params.start_point[1], z=params.travel_z, zpd=params.cut_depth)
        # repeat cut arc path
        for iteration in range(0,params.repeats + 1): # repeats start after the first
            # then cut the arc out
            self.arc_path(params)

    def not_implemented():
        raise Exception("not implemented yet")
