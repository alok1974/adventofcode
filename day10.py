# Day 10 - http://adventofcode.com/2016/day/10
import os


COMPARE_CHIPS = [17, 61]


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


class EntityType(object):
    base, bot, outbin = range(3)

    @classmethod
    def from_name(cls, name):
        if name == 'bot':
            return cls.bot
        elif name == 'output':
            return cls.outbin
        else:
            msg = 'Unable to get entity type for {0}'.format(name)
            raise ValueError(msg)

    @classmethod
    def isbot(cls, entity):
        return cls.isbottype(entity.entity_type)

    @classmethod
    def isbottype(cls, entity_type):
        return entity_type == cls.bot

    @classmethod
    def isoutbin(cls, entity):
        return cls.isoutbintype(entity.entity_type)

    @classmethod
    def isoutbintype(cls, entity_type):
        return entity_type == cls.outbin


class Entity(object):
    entity_type = EntityType.base
    max_chips = 0

    def __init__(self, uid):
        super(Entity, self).__init__()
        self.uid = uid
        self.chip_holder = []
        self.warn = False
        self.info = False

    def recieve(self, chip):
        if len(self.chip_holder) < self.max_chips:
            self.chip_holder.append(chip)
            self.chip_holder.sort()
        else:
            msg = 'Cannot recieve more than {0} chips, already holding {1}'
            raise ValueError(msg.format(self.max_chips, self.chip_holder))

        msg = '{0} recieved chip {1}'.format(self, chip)
        if self.info:
            print msg

        self.recieve_hook()

    def recieve_hook(self):
        pass

    @property
    def is_chip_holder_full(self):
        return len(self.chip_holder) == self.max_chips

    def __repr__(self):
        type_ = 'Bot' if EntityType.isbot(self) else 'OutBin'
        return '{0}({1})'.format(type_, self.uid)


class OutputBin(Entity):
    entity_type = EntityType.outbin
    max_chips = 1

    def __init__(self, uid):
        super(OutputBin, self).__init__(uid)

    @property
    def chip(self):
        if self.is_chip_holder_full:
            return self.chip_holder[0]


class Bot(Entity):
    entity_type = EntityType.bot
    max_chips = 2

    def __init__(self, uid):
        super(Bot, self).__init__(uid)
        self.low_reciever = None
        self.high_reciever = None
        self.chip_holder = []

    def recieve_hook(self):
        if self.chip_holder == COMPARE_CHIPS:
            msg = 'Part 1: {0} is comparing chips {1}'.format(
                self, self.chip_holder)
            print msg
        self.try_give()

    def set_low_reciever(self, low_reciever):
        self.low_reciever = low_reciever
        self.try_give()

    def set_high_reciever(self, high_reciever):
        self.high_reciever = high_reciever
        self.try_give()

    def try_give(self):
        if not self.low_reciever or not self.high_reciever:
            msg = (
                'Warning: {0} does not have both low and high'
                ' recievers ready yet. Cannot initiate give operation. The'
                ' operation will be tried later when both recievers are ready.'
            )
            if self.warn:
                print msg.format(self)
            return
        elif not self.is_chip_holder_full:
            msg = (
                'Chip holder for {0} is not full yet. Will try give'
                ' operation once the chip holder is full'
            )
            if self.warn:
                print msg.format(self)
            return
        else:
            self.give()

    def give(self):
        msg = '{0} Handing over chip {1} to {2} and chip {3} to {4}'.format(
            self,
            self.chip_holder[0],
            self.low_reciever,
            self.chip_holder[1],
            self.high_reciever,
        )
        if self.info:
            print msg
        self.low_reciever.recieve(self.chip_holder[0])
        self.high_reciever.recieve(self.chip_holder[1])
        self.chip_holder = []


class Entities(object):
    def __init__(self):
        self.bots = {}
        self.bins = {}

    def add(self, entity):
        if EntityType.isbot(entity):
            self.bots[entity.uid] = entity
        elif EntityType.isoutbin(entity):
            self.bins[entity.uid] = entity

    def get_bot(self, uid):
        return self.get(uid, EntityType.bot)

    def get_bin(self, uid):
        return self.get(uid, EntityType.outbin)

    def get(self, uid, entity_type, auto_create=True):
        storage = self.bots if EntityType.isbottype(entity_type) else self.bins
        entity = storage.get(uid)
        if not entity and auto_create:
            entity = self.create_entity(uid, entity_type)
            self.add(entity)

        return entity

    def create_entity(self, uid, entity_type):
        if EntityType.isbottype(entity_type):
            entity = Bot(uid)
        elif EntityType.isoutbintype(entity_type):
            entity = OutputBin(uid)
        return entity


def parse(instruction):
    if instruction.startswith('bot'):
        replacers = ['gives low to', 'and high to']
    elif instruction.startswith('value'):
        replacers = ['goes to']

    for replacer in replacers:
        instruction = instruction.replace(replacer, '')

    data = map(
        lambda x: int(x) if unicode(x).isnumeric() else x,
        instruction.split(),
    )

    out = zip(data[::2], data[1::2])
    if len(out) == 2:
        out.append((None, None))

    return tuple(out)


def main():
    entities = Entities()
    instructions = [ins for ins in get_input().split('\n') if ins.strip()]
    for instruction in instructions:
        (type1, id1), (type2, id2), (type3, id3) = parse(instruction)
        if type1 == 'value':
            bot = entities.get_bot(id2)
            bot.recieve(id1)
        else:
            bot = entities.get_bot(id1)

            low_type = EntityType.from_name(type2)
            low = entities.get(id2, low_type)
            bot.set_low_reciever(low)

            high_type = EntityType.from_name(type3)
            high = entities.get(id3, high_type)
            bot.set_high_reciever(high)

    product = reduce(
        lambda x, y: x * y,
        [entities.get_bin(uid).chip for uid in range(3)],
    )

    print 'Part 2: Product of chips in output bins 0, 1, and 2 is {0}'.format(
        product)


if __name__ == '__main__':
    main()
