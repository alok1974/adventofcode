# day5
import hashlib
import itertools


def get_hash(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


def get_password(door_id, pattern):
    pwd = [None for i in range(8)]
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


print get_password('cxdnnyjw', '00000')
