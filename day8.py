# day8
ops = """"""


class Display(object):
    def __init__(self, width=6, height=50):
        self.width = width
        self.height = height

        self.display = [
            [0 for i in range(self.width)]
            for i in range(self.height)
        ]

        self._char_map = {0: '.', 1: '#'}
        self._start_frame = '| '
        self._end_frame = ' |'

    def rect(self, x, y):
        for row in range(y):
            for column in range(x):
                self.display[row][column] = 1

    def rotate_row(self, row_num, offset):
        row = self.get_row(row_num)
        rotated = self.shift(row, offset)
        self.set_row(rotated, row_num)

    def rotate_column(self, column_num, offset):
        column = self.get_column(column_num)
        column = self.shift(column, offset)
        self.set_column(column, column_num)

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

    def shift(self, array, offset):
        for i in range(offset):
            pixel = array.pop()
            array.insert(0, pixel)
        return array

    @property
    def total_lit(self):
        num_lit = 0
        for row in self.display:
            num_lit += sum(row)
        return num_lit

    def show(self):
        out = []
        for row in self.display:
            out.append(self._start_frame)
            for pixel in row:
                out.append(self._format_pixel(pixel))
            out.append(self._end_frame)
            out.append('\n')
        print ''.join(out)

    def _format_pixel(self, pixel):
        return ' {0} '.format(self._char_map.get(pixel))


display = Display(7, 3)
display.rect(5, 2)
display.rotate_column(1, 100)
display.rotate_row(0, 4)
display.rotate_column(1, 1)
display.show()
print display.total_lit
# display.rotate_row(0, 4)
# display.show()
