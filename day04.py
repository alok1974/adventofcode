# day4
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


def get_parts(name):
    parts = name.split('-')
    letters = ''.join(parts[:-1])
    room_id = int(parts[-1].split('[')[0])
    checksum = parts[-1].split('[')[-1].split(']')[0]
    return letters, room_id, checksum


def get_checksum(letters):
    d = collections.defaultdict(int)
    for alpha in letters:
        d[alpha] += 1
    return ''.join(map(
        lambda x: x[0],
        sorted(
            sorted([(k, v) for k, v in d.items()]),
            key=lambda x: x[1],
            reverse=True,
        )[:5],
    ))


def get_sum_ids(names):
    sum_ids = 0
    for name in names:
        letters, room_id, checksum = get_parts(name)
        if checksum == get_checksum(letters):
            sum_ids += room_id
    return sum_ids


def decrypt_letters(name):
    chars = [l for l in 'abcdefghijklmnopqrstuvwxyz']
    phrase = name[:-11].split('-')
    new_phrase = []
    for word in phrase:
        decrypted = []
        for char in word:
            if char == 'z':
                decrypted.append('a')
            else:
                decrypted.append(chars[chars.index(char) + 1])
        new_phrase.append(''.join(decrypted))

    return ' '.join(new_phrase)


def main():
    names = [name for name in get_input().split('\n') if name.strip()]
    print 'Part 1: Sum of real room IDs: %s' % get_sum_ids(names)


if __name__ == '__main__':
    main()
