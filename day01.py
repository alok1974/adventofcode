# day1
import os

DIR_DEF = 'NESW'
DIRECTION = [d for d in DIR_DEF]
VISITED = []
TWICE_VISITED = None


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


def process_heading(raw_heading):
    if raw_heading not in range(-1, 5):
        msg = "Cannot process raw_heading {0}".format(raw_heading)
        raise KeyError(msg)
    elif raw_heading == -1:
        return 3
    elif raw_heading == 4:
        return 0
    else:
        return raw_heading


def heading(curr_heading, curr_transform):
    new_heading_index = process_heading(
        DIRECTION.index(curr_heading) + {'R': 1, 'L': -1}.get(curr_transform))
    return DIRECTION[new_heading_index]


def move_one_step(coords, heading):
    global TWICE_VISITED
    x, y = coords
    if heading == 'N':
        y += 1
    elif heading == 'E':
        x += 1
    elif heading == 'S':
        y -= 1
    elif heading == 'W':
        x -= 1

    new_coords = (x, y)

    if TWICE_VISITED is None:
        if new_coords in VISITED:
            TWICE_VISITED = new_coords
        VISITED.append(new_coords)

    return new_coords


def move(coords, heading, steps):
    for i in range(steps):
        coords = move_one_step(coords, heading)
    return coords


def distance(coords):
    return sum(map(abs, coords))


def parse_move(move):
    return (move[0], int(move[1:]))


def main():
    curr_heading = DIR_DEF[0]
    curr_coordinates = (0, 0)

    input_data = get_input()
    for turn, step in map(parse_move, map(str.strip, input_data.split(','))):
        curr_heading = heading(curr_heading, turn)
        curr_coordinates = move(
            curr_coordinates,
            curr_heading,
            step,
        )

    blocks = 'is {0} blocks away.'
    print 'Part 1: Easter Bunny HQ {0}'.format(blocks).format(
        distance(curr_coordinates))

    print 'Part 2: First location visited twice {0}'.format(blocks).format(
        distance(TWICE_VISITED))


if __name__ == '__main__':
    main()
