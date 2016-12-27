# Day 08 - http://adventofcode.com/2016/day/8
import os
import collections
import time


def get_input():
    day = os.path.basename(os.path.splitext(__file__)[0])
    input_file_name = '{0}.input'.format(day)
    input_file_path = os.path.abspath(
        os.path.join(__file__, '../', input_file_name)
    )

    input_data = None
    with open(input_file_path, 'r') as fp:
        input_data = fp.read()
    return input_data


class Display(object):
    off_pixel, on_pixel = range(2)

    def __init__(self, width=6, height=50):
        self.width = width
        self.height = height
        self.display = self.init_display()
        self._display_char = {self.off_pixel: ' ', self.on_pixel: '|'}
        self._start_frame = '| '
        self._end_frame = ' |'

    @classmethod
    def from_input(cls, commands, width, height):
        inst = cls(width, height)

        for command in commands:
            try:
                inst.apply_op(command)
            except IndexError:
                print 'Failed to apply command {0}'.format(command)
                raise

        return inst

    def set_display_char(self, on_char='#', off_char='.'):
        self._display_char[self.off_pixel] = off_char
        self._display_char[self.on_pixel] = on_char

    def play(self, commands):
        for command in commands:
            self.apply_op(command)
            self.show()
            time.sleep(0.05)

        time.sleep(2)
        self.blink()
        self.fade()

    def fade(self, fill=False, reverse=False):
        pixel = self.on_pixel if fill else self.off_pixel
        while True:
            for index, row in enumerate(self.display):
                row = collections.deque(row)
                if not reverse:
                    row.pop()
                    row.appendleft(pixel)
                else:
                    row.popleft()
                    row.append(pixel)
                self.set_row(list(row), index)
                self.show()
                time.sleep(0.01)

            if fill and self.total_lit == self.width * self.height:
                break
            elif self.total_lit == 0:
                break

    def blink(self, num_blinks=3):
        pixel_buffer = self.display

        for i in range(num_blinks):
            time.sleep(0.2)
            self.clear()
            self.show()
            time.sleep(0.2)
            self.set_display(pixel_buffer)
            self.show()

    def set_display(self, pixel_buffer):
        self.display = pixel_buffer

    def clear(self):
        self.display = self.init_display()

    def init_display(self):
        return [
            [0 for i in range(self.width)]
            for i in range(self.height)
        ]

    def rect(self, x, y):
        for row in range(y):
            for column in range(x):
                self.display[row][column] = 1

    def rotate_row(self, row_num, offset):
        row = self.get_row(row_num)
        rotated = self.rotate(row, offset)
        self.set_row(rotated, row_num)

    def rotate_column(self, column_num, offset):
        column = self.get_column(column_num)
        column = self.rotate(column, offset)
        self.set_column(column, column_num)

    def rotate(self, array, offset):
        array = collections.deque(array)
        array.rotate(offset)
        return list(array)

    def get_row(self, row_num):
        return self.display[row_num]

    def set_row(self, row, row_num):
        self.display[row_num] = row

    def get_column(self, column_num):
        column = []
        for row in self.display:
            for index, pixel in enumerate(row):
                if index == column_num:
                    column.append(pixel)
        return column

    def set_column(self, column, column_num):
        for row_index, row in enumerate(self.display):
            for column_index in range(len(row)):
                if column_index == column_num:
                    row[column_index] = column[row_index]

    def apply_op(self, op_string):
        if 'rect' in op_string:
            x, y = self._parse_rect_command(op_string)
            self.rect(x, y)
        else:
            num, offset = self._parse_rotate_command(op_string)
            if 'row' in op_string:
                self.rotate_row(num, offset)
            elif 'column' in op_string:
                self.rotate_column(num, offset)
            else:
                raise ValueError("cant apply op command {0}".format(op_string))

    @property
    def total_lit(self):
        num_lit = 0
        for row in self.display:
            num_lit += sum(row)
        return num_lit

    def show(self, frame=False):
        out = []
        for row in self.display:
            if frame:
                out.append(self._start_frame)
            for pixel in row:
                out.append(self._format_pixel(pixel))
            if frame:
                out.append(self._end_frame)
            out.append('\n')
        print ''.join(out)

    def _format_pixel(self, pixel):
        return '{0}'.format(self._display_char.get(pixel))

    def _parse_command(self, string, first_splitter, second_splitter):
        return map(
            int,
            map(
                str.strip,
                string.split(first_splitter)[-1].split(second_splitter),
            ),
        )

    def _parse_rotate_command(self, string):
        return self._parse_command(string, '=', 'by')

    def _parse_rect_command(self, string):
        return self._parse_command(string, 'rect', 'x')


def main():
    input_string = get_input()
    commands = [s for s in input_string.split('\n') if s.strip()]

    display = Display(50, 6)
    for command in commands:
        display.apply_op(command)
    print 'Part 1: Total lit: {0}\n'.format(display.total_lit)
    print 'Part 2: Following is display after commands - \n'
    display.show()


if __name__ == '__main__':
    main()
