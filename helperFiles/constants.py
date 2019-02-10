import pyqtgraph as pg
from dolfin import Constant


map = {}






skinnyBlackPlotPen = pg.mkPen(color=(0, 0, 0), width=1)
whitePlotPen = pg.mkPen(color=(255, 255, 255), width=2)
blackPlotPen = pg.mkPen(color=(0, 0, 0), width=2)
greyPlotPen = pg.mkPen(color=(200, 200, 200), width=2)
redPlotPen = pg.mkPen(color=(100, 0, 0), width=2)
bluePlotPen = pg.mkPen(color=(0, 0, 255), width=2)
greenPlotPen = pg.mkPen(color=(76, 153, 0), width=2)
purplePlotPen = pg.mkPen(color=(102, 0, 204), width=2)
orangePlotPen = pg.mkPen(color=(255, 128, 0), width=2)
bluePlotPen = pg.mkPen(color=(0, 0, 255), width=2)
tealPlotPen = pg.mkPen(color=(0, 204, 204), width=2)
pinkPlotPen = pg.mkPen(color=(153, 0, 153), width=2)
brownPlotPen = pg.mkPen(color=(92, 64, 51), width=2)

dataFileName = './data/GreenlandData_1_2019.h5'
cmFileName = './data/GreenlandCMData_1_2019.h5'

dt_float = 5.0  # Time step
thklim = 10.0
eps_reg = 1e-5  # Regularization parameter
dt = Constant(dt_float)
theta = Constant(0.5)  # Crank-Nicholson parameter
