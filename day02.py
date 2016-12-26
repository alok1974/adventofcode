import os


NORMAL_KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

MODIFIED_KEYPAD = [
    [None, None, 1, None, None],
    [None, 2, 3, 4, None],
    [5, 6, 7, 8, 9],
    [None, 'A', 'B', 'C', None],
    [None, None, 'D', None, None],
]


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


def clamp(val, pad_length=3):
    if val > pad_length - 1:
        return pad_length - 1
    elif val < 0:
        return 0
    return val


def get_x_y_from_num(num, keypad_to_use=NORMAL_KEYPAD):
    # print 'num to look is %s' % num
    # print 'keypad_to_use is %s' % keypad_to_use
    for y in range(len(keypad_to_use)):
        row = keypad_to_use[y]
        # print 'curr row is %s' % row
        for x in range(len(row)):
            curr_num = row[x]
            if curr_num == num:
                return y, x


def process_line(line, num, keypad_to_use=NORMAL_KEYPAD):
    pad_length = len(keypad_to_use[0])
    y, x = get_x_y_from_num(num, keypad_to_use)
    curr_num = num
    for move in line:
        step = {"U": -1, "D": 1, "R": 1, "L": -1}.get(move)
        if move in ("U", "D"):
            y += step
        else:
            x += step

        y = clamp(y, pad_length=pad_length)
        x = clamp(x, pad_length=pad_length)
        if keypad_to_use[y][x] is not None:
            curr_num = keypad_to_use[y][x]
        else:
            y, x = get_x_y_from_num(curr_num, keypad_to_use)
    return curr_num


def get_code(input_data, keypad_to_use):
    num = 5
    out = []
    for line in input_data.split('\n'):
        num = process_line(line, num, keypad_to_use=keypad_to_use)
        out.append(str(num))

    return ''.join(out)


def part1(input_data):
    return get_code(input_data, NORMAL_KEYPAD)


def part2(input_data):
    return get_code(input_data, MODIFIED_KEYPAD)


def main():
    input_data = get_input()
    print 'Part 1 code is : {0}'.format(part1(input_data))
    print 'Part 2 code is: {0}'.format(part2(input_data))


if __name__ == '__main__':
    main()
