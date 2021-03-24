import math


class Pont:
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z


def fokba(a):
    b = a * 180 / math.pi
    return b


class Kar:
    def __init__(self):
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.a4 = None
        self.l1 = 5
        self.l2 = 5
        self.l3 = 5
        self.A = Pont()
        self.B = Pont()

    def set_szogek(self, szog, P):
        self.P = P
        if (P.x == 0):
            self.a1 = math.pi / 2
        else:
            self.a1 = math.atan(P.y / P.x)
        self.B.z = P.z + math.sin(szog) * self.l3
        self.B.x = P.x - math.cos(self.a1) * (math.cos(szog) * self.l3)
        self.B.y = P.y - math.sin(self.a1) * (math.cos(szog) * self.l3)

        try:
            self.a3 = math.pi - math.acos(
                (self.l1 ** 2 + self.l2 ** 2 - self.B.x ** 2 - self.B.y ** 2 - self.B.z ** 2) / (2 * self.l1 * self.l2))
        except:
            print('Tul messze van')
            return

        self.a2 = math.asin(self.B.z / (math.sqrt(self.B.x ** 2 + self.B.y ** 2 + self.B.z ** 2))) + math.asin(
            math.sin(self.a3) * self.l2 / (math.sqrt(self.B.x ** 2 + self.B.y ** 2 + self.B.z ** 2)))

        self.A.z = math.sin(self.a2) * self.l1
        self.A.x = math.cos(self.a1) * math.cos(self.a2) * self.l1
        self.A.y = math.sin(self.a1) * math.cos(self.a2) * self.l1

        d = math.sqrt((P.x - self.A.x) ** 2 + (P.y - self.A.y) ** 2 + (P.z - self.A.z) ** 2)

        self.a4 = math.pi - math.acos((self.l3 ** 2 + self.l2 ** 2 - d ** 2) / (2 * self.l1 * self.l2))

        self.a3 = -self.a3

        Tmp = Pont()
        Tmp.x = (self.A.x + P.x) / 2
        Tmp.y = (self.A.y + P.y) / 2
        Tmp.z = (self.A.z + P.z) / 2
        if (Tmp.z < self.B.z):
            self.a4 = -self.a4

        return fokba(self.a1), fokba(self.a2), fokba(self.a3), fokba(self.a4)