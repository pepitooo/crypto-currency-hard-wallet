import argparse

import pyqrcode


class Writer:
    def __init__(self, buffer):
        self.buffer = buffer

    def add_header(self):
        pass

    def add_footer(self):
        pass

    def define_bit_as_1(self):
        pass

    def define_bit_as_0(self):
        pass

    def carrier_return(self):
        pass


class GCodeWriter(Writer):
    def __init__(self, buffer, depth, step_mm, clearance=2, feedrate=600):
        super().__init__(buffer)
        self.x_bit_position = 0
        self.y_bit_position = 0

        self.step_mm = step_mm
        self.depth = depth
        self.clearance = clearance
        self.feedrate = feedrate

    def add_header(self):
        self.buffer.write('G21 ; Set units to mm')
        self.buffer.write("\n")
        self.buffer.write('G90 ; Absolute positioning')
        self.buffer.write("\n")
        self.buffer.write('G1 Z{clearance} F{feedrate} ; Move to clearance level'.format(
            clearance=self.clearance, feedrate=self.feedrate))
        self.buffer.write("\n")

    def add_footer(self):
        self.buffer.write("M2")
        self.buffer.write("\n")

    def define_bit_as_1(self):
        self.increment_y_position()
        self.buffer.write('G1 X{xpos:.3f} Y{ypos:.3f}'.format(
            xpos=self.x_bit_position*self.step_mm, ypos=self.y_bit_position*self.step_mm))
        self.buffer.write("\n")
        self.buffer.write('G1 Z{zdown:.3f}'.format(zdown=-self.depth))
        self.buffer.write("\n")
        self.buffer.write('G1 Z{zup:.3f}'.format(zup=self.clearance))
        self.buffer.write("\n")

    def define_bit_as_0(self):
        self.increment_y_position()
        self.buffer.write('G1 X{xpos:.3f} Y{ypos:.3f}'.format(
            xpos=self.x_bit_position*self.step_mm, ypos=self.y_bit_position*self.step_mm))
        self.buffer.write("\n")

    def carrier_return(self):
        self.increment_x_position()
        self.y_bit_position = 0

    def increment_x_position(self):
        self.x_bit_position += 1

    def increment_y_position(self):
        self.y_bit_position += 1

    def new_line(self):
        self.buffer.write("\n")


def generate_gcode(text, depth, size, output_file):
    text = pyqrcode.create(text, error='H')

    print(text.terminal())

    with open(output_file, 'wt') as output:
        code = text.code
        step_mm = size / len(code)
        writer = GCodeWriter(output, depth, step_mm)
        writer.add_header()
        for row in code:
            # Each code has a quiet zone on the left side, this is the left
            # border for this code
            for bit in row:
                if bit == 1:
                    writer.define_bit_as_1()
                elif bit == 0:
                    writer.define_bit_as_0()
            writer.carrier_return()
        writer.add_footer()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate CNC QRCode GCode from a string.')
    parser.add_argument('text_to_encode', type=str, metavar='TEXT',
                        help='Text to encode in a QRCode')

    parser.add_argument('-d', '--depth', dest='depth', default=1, type=float,
                        help='Depth of each hole of QRCode')

    parser.add_argument('-s', '--size', dest='size', type=float, default=25,
                        help='Size in mm of the final QRCode')

    parser.add_argument('-o', '--output', dest='output_file', type=str, default='output.gcode',
                        help='Size in mm of the final QRCode')

    args = parser.parse_args()

    generate_gcode(text=args.text_to_encode, depth=args.depth, size=args.size, output_file=args.output_file)
    print('Generation of the GCode is done in {file}'.format(file=args.output_file))
