import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox



class Pont:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None


def fokba(a):
    b = a * 180 / math.pi
    return b

def radianba(a):
    b = a * math.pi / 180
    return b


class SliderBox:
    def __init__(self, k1, k2, k3, k4, Name, min, max , init, id):

        axe1 = plt.axes([k1, k2, k3, k4])

        self.Slider =Slider(axe1, Name, min, max, valinit=init)
        axe2 = plt.axes([k1+k3+0.005, k2, 0.09, k4])

        self.TxtBox = TextBox(axe2, '', initial=str(init))

        self.id = id
    def updateBox(self, val):
        self.TxtBox.set_val(str(round(val, 2)))
        if(self.id == 0):
            update0()

    def updateSlider(self,text):
        self.Slider.set_val(float(text))
        if (self.id == 0):
            update0()


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
        self.P = Pont()

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
            self.a3 = math.pi - math.acos((self.l1 ** 2 + self.l2 ** 2 - self.B.x ** 2 - self.B.y ** 2 - self.B.z ** 2) / (2 * self.l1 * self.l2))
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
        Tmp.x = (self.A.x + P.x)/2
        Tmp.y = (self.A.y + P.y)/2
        Tmp.z = (self.A.z + P.z)/2
        if(Tmp.z < self.B.z):
            self.a4 = -self.a4


        return fokba(self.a1), fokba(self.a2), fokba(self.a3), fokba(self.a4)



def update0():

    P.x = sliderXx.Slider.val
    P.y = sliderYy.Slider.val
    P.z = sliderZz.Slider.val
    szog = radianba(Angle.Slider.val)

    K1.set_szogek(szog, P)


    x = [0, K1.A.x, K1.B.x, P.x]
    y = [0, K1.A.y, K1.B.y, P.y]
    z = [0, K1.A.z, K1.B.z, P.z]

    ax.clear()

    ax.set_xlim3d(0, 15)
    ax.set_ylim3d(-15, 15)
    ax.set_zlim3d(-15, 15)
    ax.autoscale(enable=False)

    ax.plot(x, y, z, 'r.-')


#init
K1 = Kar()
P = Pont()
P.x = 15
P.y = 0
P.z = 0
szog = 0
K1.set_szogek(szog, P)



fig = plt.figure()
ax = fig.gca(projection='3d')
plt.subplots_adjust(bottom=0.3)
ax.set_xlim3d(0, 15)
ax.set_ylim3d(-15, 15)
ax.set_zlim3d(-15, 15)

x = [0, K1.A.x, K1.B.x, P.x]
y = [0, K1.A.y, K1.B.y, P.y]
z = [0, K1.A.z, K1.B.z, P.z]

sliderXx = SliderBox(0.25, 0.15, 0.55, 0.03, 'X', 0, 15, 15,0)
sliderYy = SliderBox(0.25, 0.1, 0.55, 0.03, 'Y', -15, 15, 0,0)
sliderZz = SliderBox(0.25, 0.05, 0.55, 0.03, 'Z', -15, 15, 0,0)
Angle = SliderBox(0.25, 0.2,0.55,0.03, 'Angle', -90,90 ,0,0)
Fog = SliderBox(0.25, 0.25,0.55,0.03, 'Grab',0,10,0,1)

#
#update
sliderXx.Slider.on_changed(sliderXx.updateBox)
sliderXx.TxtBox.on_submit(sliderXx.updateSlider)
sliderYy.Slider.on_changed(sliderYy.updateBox)
sliderYy.TxtBox.on_submit(sliderYy.updateSlider)
sliderZz.Slider.on_changed(sliderZz.updateBox)
sliderZz.TxtBox.on_submit(sliderZz.updateSlider)
Angle.Slider.on_changed(Angle.updateBox)
Angle.TxtBox.on_submit(Angle.updateSlider)
Fog.Slider.on_changed(Fog.updateBox)
Fog.TxtBox.on_submit(Fog.updateSlider)


ax.plot(x, y, z, 'r.-')

plt.show()
