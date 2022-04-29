#!/usr/bin/env python3

import argparse

import pdb
from gcode_utils import GcodeWriter

def write_key_cuts(args, gw):
    """ write the key cut loop
        cnc will slowly cut as the probe approaches template key
        once the probe hits the template go back to safe X (usually 0)
        and move up by the resolution

        assumes the cnc is currently at x0y0
        it is up to the user to zero out the grid to before starting this program
    """
    x = 0
    y = 0
    gw.block_comment(f"""key cut loop. need to cut until probe hits template key
then return to x0, then move up 1 resolution
then repeat until we have increased above the length of the cut""")
    while y < args.key_length:
        # cut until probe contact
        gw.write(f"G38.2 X10 F{args.cut_speed}")
        # return to x0 
        gw.write(f"G0 X0")
        # move up 1 * resolution
        y += args.res
        gw.write(f"G0 Y{y}")

def write_gcode(args):
    with open(args.ofile + ".gcode", 'w+') as f:
        gw = GcodeWriter(f)
        gw.comment("set to absolute motion")
        gw.write("G90")
        gw.comment("set to mm")
        gw.write("G21")
        gw.comment("turn spindle on")
        gw.write("S10000")
        write_key_cuts(args, gw)
        gw.comment("when finished go back to x0y0")
        gw.write("G0 X0 Y0")
        gw.comment("turn spindle off")
        gw.write("S0")
        gw.write("M30")

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This script will build a key cutting gcode script based on the length, width and resolution",
                                     epilog="""
    EXAMPLES:
        ./build_key_cut_gcode.py ....
        ./build_key_cut_gcode.py ....
        ./build_key_cut_gcode.py ....
    """)

    parser.add_argument("--res", "-r", default=0.5, help="resolution of line scan in mm")
    parser.add_argument("--cut-speed", default=10, help="speed of cut, should be mm/second probably integer")
    parser.add_argument("--key-length", default=10, help="length of key cut")
    parser.add_argument("--ofile", "-o", default="output", help="outputfile name without extension")
    args = parser.parse_args()
    write_gcode(args)

if __name__ == "__main__":
        main()
