from common.logger import Logger


class KeyWord(object):
    pass


class Point(KeyWord):
    # point <name> <x> <y>
    kPoint = "point"

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    @staticmethod
    def parse(txt):
        tokens = txt.split()
        if len(tokens) != 4:
            Logger().error("Wrong number of tokens")
            raise ValueError
        if str(tokens[0]).lower() != Point.kPoint:
            Logger().error("Wrong tag name")
            raise ValueError
        try:
            return Point(str(tokens[1]), int(tokens[2]), int(tokens[3]))
        except:
            Logger().error("Cannot parse point tokens")
            raise

    def __str__(self):
        return "Point [{}] x[{}] y[{}]".format(self.name, self.x, self.y)


class Line(KeyWord):
    # line <name A> <name B>
    kLine = "line"

    def __init__(self, name_a, name_b):
        self.name_a = name_a
        self.name_b = name_b

    @staticmethod
    def parse(txt):
        tokens = txt.split()
        if len(tokens) != 3:
            Logger().error("Wrong number of tokens")
        try:
            return Line(str(tokens[1]), str(tokens[2]))
        except:
            Logger().error("Cannot parse line tokens")
            raise

    def __str__(self):
        return "Line from[{}] to[{}]".format(self.name_a, self.name_b)


class Bezier(KeyWord):
    # bezier <name A> <name B> <name C> <name D>
    kBezier = "bezier"

    def __init__(self, name_a, name_b, name_c, name_d):
        self.name_a = name_a
        self.name_b = name_b
        self.name_c = name_c
        self.name_d = name_d

    @staticmethod
    def parse(txt):
        tokens = txt.split()
        if len(tokens) != 5:
            Logger().error("Wrong number of tokens")
        try:
            return Bezier(str(tokens[1]), str(tokens[2]), str(tokens[3]),
                          str(tokens[4]))
        except:
            Logger().error("Cannot parse bezier tokens")
            raise

    def __str__(self):
        return "Bezier [{}]-[{}]-[{}]-[{}]".format(self.name_a, self.name_b,
                                                   self.name_c, self.name_d)


class Circle(KeyWord):
    # circle <name A> <name B> <name C>
    kCircle = "circle"

    def __init__(self, name_a, name_b, name_c):
        self.name_a = name_a
        self.name_b = name_b
        self.name_c = name_c

    @staticmethod
    def parse(txt):
        tokens = txt.split()
        if len(tokens) != 4:
            Logger().error("Wrong number of tokens")
        try:
            return Circle(str(tokens[1]), str(tokens[2]), str(tokens[3]))
        except:
            Logger().error("Cannot parse circle tokens")
            raise

    def __str__(self):
        return "Circle with [{}]-[{}]-[{}]".format(self.name_a, self.name_b,
                                                   self.name_c)


class ConnectLeft(KeyWord):
    # connect_left <name>
    kConnectLeft = "connect_left"

    def __init__(self, name):
        self.name = name

    @staticmethod
    def parse(txt):
        tokens = txt.split()
        if len(tokens) != 2:
            Logger().error("Wrong number of tokens")
        try:
            return ConnectLeft(str(tokens[1]))
        except:
            Logger().error("Cannot parse connect_left tokens")
            raise

    def __str__(self):
        return "Connect left with[{}]".format(self.name)


class ConnectRight(KeyWord):
    # connect_right <name>
    kConnectRight = "connect_right"

    def __init__(self, name):
        self.name = name

    @staticmethod
    def parse(txt):
        tokens = txt.split()
        if len(tokens) != 2:
            Logger().error("Wrong number of tokens")
        try:
            return ConnectRight(str(tokens[1]))
        except:
            Logger().error("Cannot parse connect_right tokens")
            raise

    def __str__(self):
        return "Connect right with[{}]".format(self.name)
