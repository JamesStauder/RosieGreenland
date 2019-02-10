from constants import *


def colorToProj(x, y):
    return ((500 * x) + float(map['x'][0])), (float(map['y'][-1]) - (500 * y))



def colorCoord(x, y):
    return (-(float(map['x'][0]) - x) / 500), ((float(map['y'][-1]) - y) / 500)