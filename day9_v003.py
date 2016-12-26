# day9
import os
import collections
string = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'


def filter(string):
    return ''.join(
        [char for char in string if char.strip() and char != '\n'])


def decompress(string, outer_repeat=1):
    # string_for_last_print_statement = string[:]
    string = collections.deque(string)
    # print '\ndecompressing string: {0}'.format(''.join(string))
    # print 'outer_repeat is {0}'.format(outer_repeat)
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
            # print 'marker: {0}'.format(''.join(marker))
            num_chars, repeat = map(int, ''.join(marker).split('x'))
            # print 'num_chars: {0}, repeat: {1}'.format(num_chars, repeat)
            sub = (''.join([string.popleft() for i in range(num_chars)]))
            # print 'sub: {0}'.format(sub)
            final_count += decompress(sub, outer_repeat * repeat)
        else:
            # print "incrementing count by 1 for '{0}'".format(char)
            char_count += 1
            # print 'char_count is: {0}'.format(char_count)

    char_count *= outer_repeat
    final_count += char_count
    # print 'final count is {0}'.format(final_count)
    # print 'string was: {0}'.format(string_for_last_print_statement)

    return final_count


input_file_path = os.path.abspath(os.path.join(__file__, '../day9.input'))
with open(input_file_path, "r") as fp:
    string = filter(fp.read())

print decompress(string)
