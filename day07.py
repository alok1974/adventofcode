# day7
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


def get_parts(string):
    seqs = []
    hyper_seqs = []
    temp = []
    for char in string:
        if char == '[':
            if temp:
                seqs.append(temp)
            temp = []
        elif char == ']':
            if temp:
                hyper_seqs.append(temp)
            temp = []

        if char not in ('[', ']'):
            temp.append(char)
    if temp:
        seqs.append(temp)

    return [''.join(sq) for sq in seqs], [''.join(sq) for sq in hyper_seqs]


def is_aba(group):
    a, b, c = group
    return a == c


def reverse_aba(group):
    a, b, c = group
    return ''.join([b, a, b])


def is_abba(group):
    a, b, c, d = group
    return a == d and b == c and a != b


def has_abba(string):
    for index in range(len(string) - 3):
        grp = string[index: index + 4]
        if is_abba(grp):
            return True
    return False


def get_abas(string):
    abas = []
    for index in range(len(string) - 2):
        grp = string[index: index + 3]
        if is_aba(grp):
            abas.append(grp)
    return abas


def get_abas_from_sqs(sqs):
    sq_abas = []
    for sq in sqs:
        for abas in get_abas(sq):
            sq_abas.append(abas)
    return sq_abas


def abas_in_sqs(seqs):
    for seq in seqs:
        return get_abas(seq)


def sqs_have_abba(seqs):
    for seq in seqs:
        if has_abba(seq):
            return True


def get_num_TLS(ips):
    num_TLS = 0
    for ip in ips:
        seqs, hyper_seqs = get_parts(ip)
        if not sqs_have_abba(hyper_seqs) and sqs_have_abba(seqs):
            num_TLS += 1

    return num_TLS


def get_num_SSL(ips):
    num_SSL = 0
    for ip in ips:
        seqs, hyper_seqs = get_parts(ip)
        seq_abas = get_abas_from_sqs(seqs)
        hyper_abas = get_abas_from_sqs(hyper_seqs)
        if set(seq_abas).intersection(set(map(reverse_aba, hyper_abas))):
            num_SSL += 1
    return num_SSL


def main():
    ips = [ip for ip in get_input().split('\n') if ip.strip()]
    print 'Part 1: Total TLS: {0}'.format(get_num_TLS(ips))
    print 'Part 2: Total SSL: {0}'.format(get_num_SSL(ips))


if __name__ == '__main__':
    main()
