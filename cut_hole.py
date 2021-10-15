#!/usr/bin/env python3

import argparse

import pdb
from gcode_utils import GcodeWriter
from path_primitives import CirclePath

def write_gcode(args):
    gw = GcodeWriter(args.ofile)
    gw.set_absolute_motion()
    gw.set_units("mm")

    gw.comment("goto safe place")
    gw.goto(x=0, y=0, z=15)
    gw.comment("cut circle")
    cp = CirclePath(gcode_writer=gw, center=[0,0], r=args.radius, f=args.cut_speed, bit_width=args.bit_width)
    cp.cut_arc()

    gw.comment("when finished go back to x0y0zsafe")
    gw.goto(x=0, y=0, z=15)
    gw.set_spindle_speed(0)
    gw.end_program()

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This script will build a hole cutting gcode script based on the length, width and resolution",
                                     epilog="""
    EXAMPLES:
        ./build_key_cut_gcode.py ....
        ./build_key_cut_gcode.py ....
        ./build_key_cut_gcode.py ....
    """)

    # parser.add_argument("--res", "-r", default=0.5, help="resolution of line scan in mm")
    parser.add_argument("--cut-speed", default=10, help="speed of cut, should be mm/second probably integer")
    # parser.add_argument("--key-length", default=10, help="length of key cut")
    parser.add_argument("--radius", "-r", default=1, type=float, help="radius of arc")
    parser.add_argument("--bit-width", default=1, type=float, help="width of cutting bit")
    parser.add_argument("--ofile", "-o", default="output", help="outputfile name without extension")
    args = parser.parse_args()
    pdb.set_trace
    write_gcode(args)

if __name__ == "__main__":
        main()
