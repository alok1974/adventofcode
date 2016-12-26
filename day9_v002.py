# day9
import os
import collections
string = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
grp1 = '(3x3)ABC(2x3)XY(5x2)PQRST'
grp2 = '(18x9)(3x2)TWO(5x7)SEVEN'


def filter(string):
    return ''.join(
        [char for char in string if char.strip() and char != '\n'])


def decompress(string, count=0):
    string = collections.deque(string)
    marker = []
    result = ''
    group = ''
    while len(string):
        char = string.popleft()
        if char == '(':
            while True:
                marker_char = string.popleft()
                if marker_char == ')':
                    break
                marker.append(marker_char)
            num_chars, repeat = map(int, ''.join(marker).split('x'))
            for i in range(num_chars):
                group = ''.join([group, string.popleft()])
            count += num_chars * repeat
            for i in range(repeat):
                result = ''.join([result, group])
            marker = []
            group = ''
        else:
            count += 1
            result = ''.join([result, char])
    return count, result


input_file_path = os.path.abspath(os.path.join(__file__, '../day9.input'))
with open(input_file_path, "r") as fp:
    string = filter(fp.read())

while True:
    count, string = decompress(string)
    if '(' not in string:
        print count
        break
