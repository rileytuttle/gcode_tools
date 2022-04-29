#!/usr/bin/env python3

import pdb
from gcode_utils import GcodeWriter

def main():
    ofile = "channel_cut.gcode"
    with open(ofile, 'w+') as f:
        gw = GcodeWriter(f)    
        gw.set_absolute_motion()
        gw.set_units("mm")
        gw.comment("turn spindle on")
        gw.set_spindle_speed(10000)

        """ loop through from 0 to distance we want.
        """
        bit_width = 3
        overlap = 0.25
        total_length = 168
        total_height = 154
        top_bottom_buffer = 10
        cut_depth = 10
        for current_cut in range(0, cut_depth):
            gw.comment("starting new layer")
            # assume starting with center of bit at like x,y,z = 0, 3, 0
            # put side of bit on start line and below (y direction) the wood
            gw.goto(x=1.5, y=-10)
            gw.goto(z=-(current_cut+1), f=10) # plunge bit
            direction = "up" # first cut is up
            # the current edge of bit. so after the first cut we should be at 3
            current = 3
            while current <= total_length:
                if direction == "up":
                    gw.goto(y=total_height + top_bottom_buffer, f=10)
                    direction = "down"
                elif direction == "down":
                    gw.goto(y=0-top_bottom_buffer, f=10)
                    direction = "up"
                next_x = current + bit_width/2 - overlap
                gw.goto(x=next_x) # after the cut we move the bit to current
                current = next_x + bit_width/2
        
        gw.comment("when finished go back to x0y0z{safe}")
        gw.goto(z=10)
        gw.goto(x=0,y=0)
        gw.comment("turn spindle off")
        gw.set_spindle_speed(0)
        # end program .. I think?        
        gw.write("M30")

if __name__ == "__main__":
        main()
