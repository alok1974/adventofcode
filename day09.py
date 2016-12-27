# day9
import os
import collections


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


def filter(string):
    return ''.join(
        [char for char in string if char.strip() and char != '\n'])


def decompress01(string, count=0):
    string = collections.deque(string)
    marker = []
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
            marker = []
            group = ''
        else:
            count += 1
    return count


def decompress02(string, outer_repeat=1):
    string = collections.deque(string)
    final_count = 0
    char_count = 0
    while len(string):
        char = string.popleft()
        if char == '(':
            marker = []
            while True:
                marker_char = string.popleft()
                if marker_char == ')':
                    break
                marker.append(marker_char)
            num_chars, repeat = map(int, ''.join(marker).split('x'))
            sub = (''.join([string.popleft() for i in range(num_chars)]))
            final_count += decompress02(sub, outer_repeat * repeat)
        else:
            char_count += 1

    char_count *= outer_repeat
    final_count += char_count

    return final_count


def main():
    string = filter(get_input())

    print 'Part 1: length is: {0}'.format(decompress01(string))
    print 'Part 2: length is : {0}'.format(decompress02(string))


if __name__ == '__main__':
    main()
