import os


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


def is_tri(tri):
    smallest_side = min(tri)
    largest_side = max(tri)
    tri.remove(smallest_side)
    tri.remove(largest_side)
    remaining_side = tri[0]
    return smallest_side + remaining_side > largest_side


def part_1(input_data):
    num_valid = 0
    for tri in map(lambda x: map(int, x), map(str.split, input_data)):
        if is_tri(tri):
            num_valid += 1
    return num_valid


def part_2(input_data):
    num_valid = 0
    tris = []
    for data in map(lambda x: map(int, x), map(str.split, input_data)):
        tris.append(data)
        if len(tris) == 3:
            first_tri = [l[0] for l in tris]
            second_tri = [l[1] for l in tris]
            third_tri = [l[2] for l in tris]
            for tri in [first_tri, second_tri, third_tri]:
                if is_tri(tri):
                    num_valid += 1
            tris = []
    return num_valid


def main():
    input_data = [x for x in get_input().split('\n') if x.strip()]
    print 'Part 1: Total Valid Triangles are {0}'.format(part_1(input_data))
    print 'Part 2: Total Valid Triangles are {0}'.format(part_2(input_data))


if __name__ == '__main__':
    main()
