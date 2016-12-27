# Day 05 - http://adventofcode.com/2016/day/5
import os
import hashlib
import itertools


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


def get_hash(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


def get_password_part01(door_id, pattern, maxlen=8):
    pwd = []
    for i in itertools.count():
        hash = get_hash('{0}{1}'.format(door_id, i))
        if hash.startswith(pattern):
            pwd.append(hash[5])

        if len(pwd) == maxlen:
            return ''.join(pwd)


def get_password_part02(door_id, pattern, maxlen=8):
    pwd = [None for i in range(maxlen)]
    for i in itertools.count():
        hash = get_hash('{0}{1}'.format(door_id, i))
        if hash.startswith(pattern):
            try:
                pos = int(hash[5])
            except ValueError:
                pass
            else:
                if pos in xrange(8) and pwd[pos] is None:
                    pwd[pos] = hash[6]

        if all(pwd):
            return ''.join(pwd)


def main():
    door_id = get_input()
    startswith_pattern = '00000'
    print 'Part 1: Password is: {0}'.format(
        get_password_part01(door_id, startswith_pattern))
    print 'Part 2: Password is: {0}'.format(
        get_password_part02(door_id, startswith_pattern))


if __name__ == '__main__':
    main()
