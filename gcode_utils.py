import pdb
class GcodeWriter():
    def __init__(self, filehandle):
        self.filehandle = filehandle
        self.units = "mm"
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
            self.write("G21")
        elif units == "in":
            self.not_implemented()
        else:
            self.not_implemented()
    def set_spindle_speed(self, speed):
        self.write(f"S{speed}")
    def goto(self, x=None, y=None, z=None, f=None):
        if x is None and y is None and z is None:
            raise Exception("go nowhere ?")
        if f is None:
            cmd = "G0"
        else:
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
    def cut_circle(self, x, y, z, f):
        not_implemented()
    def not_implemented():
        raise Exception("not implemented yet")
            

      
            
