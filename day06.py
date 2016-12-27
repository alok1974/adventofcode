# day6
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


def parse_messages(messages):
    columns = [collections.defaultdict(int) for i in range(len(messages[0]))]
    for message in messages:
        for index, char in enumerate(message):
            columns[index][char] += 1
    return columns


def filter_noise(parsed_message, most_common=True):
    index = 0 if most_common else -1
    filtered = []
    for column in parsed_message:
        filtered.append(
            sorted(
                column.keys(),
                key=lambda x: column.get(x),
                reverse=True,
                )[index],
        )

    return ''.join(filtered)


def main():
    messages = [m for m in get_input().split('\n') if m.strip()]
    message_data = parse_messages(messages)
    print 'Part 1: Message is {0}'.format(filter_noise(message_data))
    print 'Part 2: Message is {0}'.format(
        filter_noise(message_data, most_common=False))


if __name__ == '__main__':
    main()
