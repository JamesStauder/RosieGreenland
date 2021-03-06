from PyQt4.QtGui import *
import math
from Instructions import *
from FlowIntegrator import *
from Dataset import *
from Marker import *
from ModelGUI import *
from ..caching.cachingFunctions import *
import time
from Square import *
from pyproj import Proj
'''
Class: MainWindow
Argument list:
Purpose: Create main window for GUI. Has many functions based on what user does
Return types, values:
Dependencies: pyQT, dolfin, math
Creator: James Stauder
Date created: 1/31/18
Last edited: 5/29/18
'''


class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Greenland")
        self.setMinimumHeight(1000)
        self.setMinimumWidth(1200)

        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QtGui.QHBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # index of current map
        self.currentMap = 0

        # marker selected variables
        self.isMarkerSelected = False
        self.whichMarkerSelected = None
        self.selectedMarkerPosition = None
        self.whichIndexOfFlowlineSelected = None

        # Flowline information
        self.flowlineDistance = 100000
        self.lengthOfFlowline = 1
        self.flowlines = []
        self.flowlineMarkers = []
        self.integratorPerMarker = 1

        '''
        Side widget with button
        '''
        self.maxWidth = 300

        self.buttonBoxWidget = QtGui.QWidget()
        self.buttonBox = QtGui.QVBoxLayout()
        self.buttonBoxWidget.setLayout(self.buttonBox)

        self.mapList = QtGui.QComboBox()
        self.maps = ['Velocity', 'Bed', 'Surface', 'SMB', 'Thickness', 't2m']
        self.mapList.addItems(self.maps)
        self.mapList.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.mapList)

        self.spatialResolutionWidget = QtGui.QWidget()
        self.spatialResolutionLayout = QtGui.QHBoxLayout()
        self.spatialResolutionWidget.setLayout(self.spatialResolutionLayout)
        self.spatialResolutionLabel = QtGui.QLabel('Spatial Resolution(m)')
        self.spatialResolutionLineEdit = QtGui.QLineEdit('1000')
        self.spatialResolutionLayout.addWidget(self.spatialResolutionLabel)
        self.spatialResolutionLayout.addWidget(self.spatialResolutionLineEdit)
        self.buttonBox.addWidget(self.spatialResolutionWidget)

        self.distanceWidget = QtGui.QWidget()
        self.distanceLayout = QtGui.QHBoxLayout()
        self.distanceWidget.setLayout(self.distanceLayout)
        self.distanceLabel = QtGui.QLabel('distance(km)')
        self.distanceLineEdit = QtGui.QLineEdit('100')
        self.spatialResolutionLayout.addWidget(self.distanceLabel)
        self.spatialResolutionLayout.addWidget(self.distanceLineEdit)
        self.buttonBox.addWidget(self.distanceWidget)


        self.upButton = QRadioButton('Integrate Up')
        self.downButton = QRadioButton('Integrate Down')
        self.upButton.setChecked(True)
        self.buttonBox.addWidget(self.upButton)
        self.buttonBox.addWidget(self.downButton)


        self.averageWidget = QtGui.QWidget()
        self.averageLayout = QtGui.QHBoxLayout()
        self.averageWidget.setLayout(self.averageLayout)
        self.widthAverageButton = QtGui.QCheckBox('Use Width Average')
        self.widthAverageButton.setTristate(False)
        self.averageLayout.addWidget(self.widthAverageButton)
        self.buttonBox.addWidget(self.averageWidget)

        self.profileWidget = QtGui.QWidget()
        self.profileLayout = QtGui.QHBoxLayout()
        self.profileWidget.setLayout(self.profileLayout)
        self.profileLabel = QtGui.QLabel('output file name')
        self.profileLineEdit = QtGui.QLineEdit('myProfile.h5')
        self.profileLayout.addWidget(self.profileLabel)
        self.profileLayout.addWidget(self.profileLineEdit)
        self.buttonBox.addWidget(self.profileWidget)

        self.instructionButton = QtGui.QPushButton('Instructions')
        self.instructionButton.setEnabled(True)
        self.instructionButton.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.instructionButton)

        self.plotPathButton = QtGui.QPushButton('Plot Path')
        self.plotPathButton.setEnabled(False)
        self.plotPathButton.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.plotPathButton)

        self.runModelButton = QtGui.QPushButton('Run Model')
        self.runModelButton.setEnabled(False)
        self.runModelButton.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.runModelButton)

        self.resetButton = QtGui.QPushButton('Reset')
        self.resetButton.setEnabled(True)
        self.resetButton.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.resetButton)

        self.velocityWidthButton = QtGui.QPushButton('Create Profile')
        self.velocityWidthButton.setEnabled(False)
        self.velocityWidthButton.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.velocityWidthButton)


        self.rosieButton = QtGui.QPushButton('Super special Rosie Button')
        self.rosieButton.setEnabled(False)
        self.rosieButton.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.rosieButton)


        self.latLongWidget = QtGui.QWidget()
        self.latLongLayout = QtGui.QHBoxLayout()
        self.latLongWidget.setLayout(self.latLongLayout)
        self.latLabel = QtGui.QLabel('Lat')
        self.latLineEdit = QtGui.QLineEdit('')
        self.longLabel = QtGui.QLabel('Long')
        self.longLineEdit = QtGui.QLineEdit('')
        self.latLongLayout.addWidget(self.latLabel)
        self.latLongLayout.addWidget(self.latLineEdit)
        self.latLongLayout.addWidget(self.longLabel)
        self.latLongLayout.addWidget(self.longLineEdit)
        self.latLongButton = QtGui.QPushButton('Find Lat Long')

        self.buttonBox.addWidget(self.latLongWidget)
        self.buttonBox.addWidget(self.latLongButton)

        self.latLongWidget2 = QtGui.QWidget()
        self.latLongLayout2 = QtGui.QHBoxLayout()
        self.latLongWidget2.setLayout(self.latLongLayout2)
        self.latLabel2 = QtGui.QLabel('Lat')
        self.latLineEdit2 = QtGui.QLineEdit('')
        self.longLabel2 = QtGui.QLabel('Long')
        self.longLineEdit2 = QtGui.QLineEdit('')
        self.latLongLayout2.addWidget(self.latLabel2)
        self.latLongLayout2.addWidget(self.latLineEdit2)
        self.latLongLayout2.addWidget(self.longLabel2)
        self.latLongLayout2.addWidget(self.longLineEdit2)
        self.latLongButton2 = QtGui.QPushButton('Plot Location')

        self.buttonBox.addWidget(self.latLongWidget2)
        self.buttonBox.addWidget(self.latLongButton2)

        self.textOut = QtGui.QTextBrowser()
        self.textOut.setMaximumWidth(self.maxWidth)
        self.buttonBox.addWidget(self.textOut)

        self.leftSideWidget = QtGui.QWidget()
        self.leftSide = QtGui.QVBoxLayout()
        self.leftSideWidget.setLayout(self.leftSide)

        self.imageItemContainer = QtGui.QStackedWidget()

        self.leftSide.addWidget(self.imageItemContainer)

        self.mainLayout.addWidget(self.leftSideWidget)
        self.mainLayout.addWidget(self.buttonBoxWidget)

        self.buttonBoxWidget.setMaximumWidth(self.maxWidth + 12)

        self.connectButtons()

    '''
    Function: addToImageItemContainer
    Argument list: datasetDict
    Purpose: add the different dataset widgets to the imageItemContainer
    Return types, values: 
    Dependencies: 
    Creator: James Stauder
    Date created: 2/25/18
    Last edited: 3/5/18
    '''

    def addToImageItemContainer(self, datasetDict):
        self.imageItemContainer.addWidget(datasetDict['velocity'].plotWidget)
        self.imageItemContainer.setCurrentWidget(datasetDict['velocity'].plotWidget)

        self.imageItemContainer.addWidget(datasetDict['bed'].plotWidget)
        self.imageItemContainer.addWidget(datasetDict['surface'].plotWidget)
        self.imageItemContainer.addWidget(datasetDict['thickness'].plotWidget)
        self.imageItemContainer.addWidget(datasetDict['t2m'].plotWidget)
        self.imageItemContainer.addWidget(datasetDict['smb'].plotWidget)


    '''
    Function: changeMap
    Argument list: 
        index: index of which map to use
    Purpose: Changes the map to a different colormap
    Return types, values: 
    Dependencies: 
    Creator: James Stauder
    Date created: 2/25/18
    Last edited: 3/5/18
    '''

    def changeMap(self, index):
        vr = self.imageItemContainer.currentWidget().getPlotItem().getViewBox().viewRange()
        indexToDatasetDict = {
            0: 'velocity',
            1: 'bed',
            2: 'surface',
            3: 'smb',
            4: 'thickness',
            5: 't2m'}
        if index != self.currentMap:
            oldMap = self.currentMap
            self.currentMap = index

        self.imageItemContainer.setCurrentWidget(self.datasetDict[indexToDatasetDict[self.currentMap]].plotWidget)
        self.datasetDict[indexToDatasetDict[self.currentMap]].imageItem.hoverEvent = self.mouseMove
        self.datasetDict[indexToDatasetDict[self.currentMap]].imageItem.mouseClickEvent = self.mouseClick

        self.datasetDict[indexToDatasetDict[self.currentMap]].plotWidget.getPlotItem().getViewBox().setRange(
            xRange=vr[0],
            yRange=vr[1],
            padding=0.0)
        for line in self.flowlineMarkers:
            for marker in line:
                marker.plotWidget = self.datasetDict[indexToDatasetDict[self.currentMap]]
                self.datasetDict[indexToDatasetDict[oldMap]].plotWidget.removeItem(marker.cross[0])
                self.datasetDict[indexToDatasetDict[oldMap]].plotWidget.removeItem(marker.cross[1])
                self.datasetDict[indexToDatasetDict[self.currentMap]].plotWidget.addItem(marker.cross[0])
                self.datasetDict[indexToDatasetDict[self.currentMap]].plotWidget.addItem(marker.cross[1])

                if marker.lines[0]:
                    self.datasetDict[indexToDatasetDict[self.currentMap]].plotWidget.addItem(marker.lines[0])

    '''
     Function: mouseClick
     Argument list: 
        e: event trigger from mouse being clicked
     Purpose: 
        Create a new flowline or move a previous flowline
     Return types, values: None
     Dependencies: None
     Creator: James Stauder
     Date created: 2/25/18
     Last edited: 5/29/18
     '''

    def mouseClick(self, e):

        # If no marker is selected
        if self.isMarkerSelected is False:

            # Check to see if click selects a marker. If so memoize the marker and the flowline Position
            # This block checks every marker along flowline and reintegrates up. Commented out with new
            # averaging method
            '''
            for i in range(len(self.flowlineMarkers)):
                for j in range(len(self.flowlineMarkers[i])):
                    if self.flowlineMarkers[i][j].checkClicked(e.pos()):
                        self.isMarkerSelected = True
                        self.whichMarkerSelected = self.flowlineMarkers[i][j]
                        self.selectedMarkerPosition = [i, j]

                        self.displayMarkerVariables()
                        tempX, tempY = self.whichMarkerSelected.dx, self.whichMarkerSelected.dy
                        for k in range(len(self.flowlines[i])):
                            if self.flowlines[i][k] == [tempX, tempY]:
                                self.whichIndexOfFlowlineSelected = [i, k]
                        break
            '''
            self.rosieButton.setEnabled(True)
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            if self.downButton.isChecked():
                self.flowIntegrator.direction = 1
            else:
                self.flowIntegrator.direction = -1
            # Checks to see only if first marker in each flowline is detected.
            for i in range(len(self.flowlineMarkers)):
                if self.flowlineMarkers[i][0].checkClicked(e.pos()):
                    self.isMarkerSelected = True
                    self.whichMarkerSelected = self.flowlineMarkers[i][0]
                    self.selectedMarkerPosition = [i, 0]

                    self.displayMarkerVariables()
                    self.whichIndexOfFlowlineSelected = [i, 0]
                    break

            # If no marker selected previously or currently create new flowline. Also cannot create more
            # then 2 flowlines.
            if (len(self.flowlines) < 1) and self.isMarkerSelected is False:
                self.spatialResolutionLineEdit.setReadOnly(True)
                self.distanceLineEdit.setReadOnly(True)
                self.flowlineDistance = int(self.distanceLineEdit.text()) * 1000
                self.lengthOfFlowline = int(self.flowlineDistance / float(self.spatialResolutionLineEdit.text()))
                xClickPosition = e.pos().x()
                yClickPosition = e.pos().y()

                dx, dy = colorToProj(xClickPosition, yClickPosition)

                # Create new flowline
                newFlowline = []
                for x in range(0, self.lengthOfFlowline):
                    newFlowline.append(None)
                newFlowline[0] = [dx, dy]

                newFlowline = self.flowIntegrator.integrate(dx, dy, newFlowline, 0,
                                                            float(self.spatialResolutionLineEdit.text()))

                if None in newFlowline:
                    print "Integration Error. Try Again"
                    return


                # Create a flowline of markers spaced out based on the IntegratorPerMarker
                newFlowlineMarkers = newFlowline[::self.integratorPerMarker]

                for i in range(len(newFlowlineMarkers)):
                    dx = newFlowlineMarkers[i][0]
                    dy = newFlowlineMarkers[i][1]
                    cx, cy = colorCoord(dx, dy)
                    newFlowlineMarkers[i] = Marker(cx, cy, dx, dy, self.imageItemContainer.currentWidget())

                self.displayMarkers(newFlowlineMarkers)

                self.flowlines.append(newFlowline)
                self.flowlineMarkers.append(newFlowlineMarkers)


        # Release the marker that was previously held
        else:
            self.isMarkerSelected = False
            self.whichMarkerSelected = None
            self.textOut.clear()

    '''
    Function: mouseMove
    Argument list: 
    Purpose: This function is used to move the marker that is selected and create a new integration path. 
    Return types, values: 
    Dependencies: 
    Creator: James Stauder
    Date created: 2/25/18
    Last edited: 3/9/18
    TODO: 
        This can be a bit confusing to read. The code is kind of wordy. We could possibly redraw flowline with the 
        display Markers function but that would require some changes to the Markers function to take an index.
    '''

    def mouseMove(self, e):

        if self.isMarkerSelected:

            # change the x , y values of the marker at the selected index
            xPositionOfCursor = e.pos().x()
            yPositionOfCursor = e.pos().y()
            self.whichMarkerSelected.cx = xPositionOfCursor
            self.whichMarkerSelected.cy = yPositionOfCursor
            self.whichMarkerSelected.updateCross()

            # change the x, y values of the flowline at the selected index
            whichFlowlineSelected = self.whichIndexOfFlowlineSelected[0]
            indexSelected = self.whichIndexOfFlowlineSelected[1]
            self.flowlines[whichFlowlineSelected][indexSelected] = [self.whichMarkerSelected.dx,
                                                                    self.whichMarkerSelected.dy]

            self.flowlines[whichFlowlineSelected] = self.flowIntegrator.integrate(
                self.whichMarkerSelected.dx, self.whichMarkerSelected.dy,
                self.flowlines[whichFlowlineSelected], indexSelected,
                float(self.spatialResolutionLineEdit.text()))

            # Remove every marker past the one we selected
            for i in range(self.selectedMarkerPosition[1] + 1, len(self.flowlineMarkers[0])):
                self.imageItemContainer.currentWidget().removeItem(
                    self.flowlineMarkers[self.selectedMarkerPosition[0]][i])

                # get the flowline position of the new marker
                newPosition = self.flowlines[whichFlowlineSelected][i * self.integratorPerMarker]
                cx, cy = colorCoord(newPosition[0], newPosition[1])

                # Create new marker with new data
                self.flowlineMarkers[self.selectedMarkerPosition[0]][i] = Marker(
                    cx, cy, newPosition[0], newPosition[1],
                    self.imageItemContainer.currentWidget())
            # This section redraws the new markers
            for i in range(self.selectedMarkerPosition[1] + 1, len(self.flowlineMarkers[0])):
                self.imageItemContainer.currentWidget().addItem(
                    self.flowlineMarkers[self.selectedMarkerPosition[0]][i].getCross()[0])
                self.imageItemContainer.currentWidget().addItem(
                    self.flowlineMarkers[self.selectedMarkerPosition[0]][i].getCross()[1])

                xa = [self.flowlineMarkers[self.selectedMarkerPosition[0]][i - 1].cx,
                      self.flowlineMarkers[self.selectedMarkerPosition[0]][i].cx]
                ya = [self.flowlineMarkers[self.selectedMarkerPosition[0]][i - 1].cy,
                      self.flowlineMarkers[self.selectedMarkerPosition[0]][i].cy]
                self.flowlineMarkers[self.selectedMarkerPosition[0]][i].setLine(
                    pg.PlotDataItem(xa, ya, connect='all', pen=skinnyBlackPlotPen), 0)
                self.flowlineMarkers[self.selectedMarkerPosition[0]][i - 1].setLine(
                    self.flowlineMarkers[self.selectedMarkerPosition[0]][i].lines[0], 1)

                self.imageItemContainer.currentWidget().addItem(
                    self.flowlineMarkers[self.selectedMarkerPosition[0]][i].lines[0])

            self.displayMarkerVariables()

            # Connect lines between marker selected and previous marker
            if self.whichMarkerSelected.lines[0] is not None:
                self.whichMarkerSelected.lines[0].setData(
                    [self.whichMarkerSelected.lines[0].getData()[0][0], self.whichMarkerSelected.cx],
                    [self.whichMarkerSelected.lines[0].getData()[1][0], self.whichMarkerSelected.cy])

    '''
    Function: calcVelocityWidth
    Argument list: 
    Purpose: 
        Calculates velocity width by connecting the ith marker of each shear margin. This displays lines between
        each displayed marker as well. This also does an averaging scheme where we create lines between the two shear
        margins starting at the terminus. The number of lines is determined by numberOfLines. The averaging is done
        by averaging the ith index of each line together.
        TODO: Reference paper when written
    Return types, values: 
    Dependencies: Two selected shear margins. This is susceptible to user errors. TODO: Fix the errors
    Creator: James Stauder
    Date created: 2/25/18
    Last edited: 3/9/18
    '''

    def calcVelocityWidth(self):

        x1, y1 = self.flowlineMarkers[0][0].cx, self.flowlineMarkers[0][0].cy
        x2, y2 = self.flowlineMarkers[1][0].cx, self.flowlineMarkers[1][0].cy

        numberOfLines = 100

        dx = (x2 - x1) / numberOfLines
        dy = (y2 - y1) / numberOfLines
        currX = x1
        currY = y1

        # Create center flowlines
        t0 = time.time()
        for _ in range(0, numberOfLines-1):
            currX = currX + dx
            currY = currY + dy

            xProj, yProj = colorToProj(currX, currY)

            newLine = []

            for i in range(self.lengthOfFlowline):
                newLine.append(None)
            newLine[0] = [xProj, yProj]
            newLine = self.flowIntegrator.integrate(xProj, yProj, newLine, 0,
                                                    float(self.spatialResolutionLineEdit.text()))

            #This checks to see if integration worked
            if None not in newLine:
                self.flowlines.append(newLine)
            else:
                print "integration error on averaging method. Ommitting line"



            #Code to create Markers for these flowlines.
            '''
            newFlowlineMarkers = newLine[::self.integratorPerMarker]
            for i in range(len(newFlowlineMarkers)):
                dataX = newFlowlineMarkers[i][0]
                dataY = newFlowlineMarkers[i][1]
                cx, cy = colorCoord(dataX, dataY)
                newFlowlineMarkers[i] = Marker(cx, cy, dataX, dataY, self.imageItemContainer.currentWidget())
            self.displayMarkers(newFlowlineMarkers)
            self.flowlineMarkers.append(newFlowlineMarkers)
            


        for i in range(len(self.flowlineMarkers[0])):
            for j in range(3, len(self.flowlines)):
                xValues = [self.flowlineMarkers[j - 1][i].cx, self.flowlineMarkers[j][i].cx]
                yValues = [self.flowlineMarkers[j - 1][i].cy, self.flowlineMarkers[j][i].cy]

                self.flowlineMarkers[j][i].setLine(
                    pg.PlotDataItem(xValues, yValues, connect='all', pen=skinnyBlackPlotPen), 0)
                self.imageItemContainer.currentWidget().addItem(self.flowlineMarkers[j][i].lines[0])

            xValues = [self.flowlineMarkers[0][i].cx, self.flowlineMarkers[2][i].cx]
            yValues = [self.flowlineMarkers[0][i].cy, self.flowlineMarkers[2][i].cy]

            self.flowlineMarkers[0][i].setLine(pg.PlotDataItem(xValues, yValues, connect='all', pen=skinnyBlackPlotPen),
                                               0)
            self.imageItemContainer.currentWidget().addItem(self.flowlineMarkers[0][i].lines[0])

            xValues = [self.flowlineMarkers[1][i].cx, self.flowlineMarkers[len(self.flowlines) - 1][i].cx]
            yValues = [self.flowlineMarkers[1][i].cy, self.flowlineMarkers[len(self.flowlines) - 1][i].cy]

            self.flowlineMarkers[1][i].setLine(pg.PlotDataItem(xValues, yValues, connect='all', pen=skinnyBlackPlotPen),
                                               0)
            self.imageItemContainer.currentWidget().addItem(self.flowlineMarkers[1][i].lines[0])
            '''




        print "Ommitted ", numberOfLines - len(self.flowlines) + 1, " lines. Out of a possible ", numberOfLines-1
        midFlowline = self.flowlines[((len(self.flowlines) - 2) / 2) + 2]


        newFlowlineMarkers = midFlowline[::self.integratorPerMarker]

        for i in range(len(newFlowlineMarkers)):
            dx = newFlowlineMarkers[i][0]
            dy = newFlowlineMarkers[i][1]
            cx, cy = colorCoord(dx, dy)
            newFlowlineMarkers[i] = Marker(cx, cy, dx, dy, self.imageItemContainer.currentWidget())

        self.displayMarkers(newFlowlineMarkers)
        self.flowlineMarkers.append(newFlowlineMarkers)

        self.runModelButton.setEnabled(True)
        self.velocityWidthButton.setEnabled(False)

        vAll = []

        for line in range(len(self.flowlines)):
            v = []
            for point in range(len(self.flowlines[0])):
                v.append(self.datasetDict['velocity'].getInterpolatedValue(self.flowlines[line][point][0],
                                                                           self.flowlines[line][point][1])[0][0])
            vAll.append(v)

        midLine = []
        for point in range(len(self.flowlines[0])):
            midLine.append(self.datasetDict['velocity'].getInterpolatedValue(self.flowlines[2][point][0],
                                                                       self.flowlines[2][point][1])[0][0])
        avg = []
        for point in range(len(vAll[0])):
            tot = 0
            for line in range(len(vAll)):
                tot += vAll[line][point]
            avg.append(tot/len(vAll[0]))

        minIndex = 0
        for point in avg:
            if point < 120:
                break
            minIndex += 1
        maxIndex = minIndex
        for point in avg[minIndex:]:
            if point < 50:
                break
            maxIndex += 1

        dx = 1000
        dy = np.diff(avg)/dx
        dy2 = np.diff(midLine)/dx
        interpolateFlowlineData(self.datasetDict, self.flowlines,midFlowline, self.flowlineDistance,
                                float(self.spatialResolutionLineEdit.text()), self.profileLineEdit.text())
        print "Profile creation took :", time.time() - t0

    '''
    Function: displayMarkers
    Argument list: 
        flowline: flowline in which to display
    Purpose: Takes a flowline of markers and displays them on the gui
    Return types, values: None
    Dependencies: None
    Creator: James Stauder
    Date created: 3/2/18
    Last edited: 3/2/18
    '''

    def displayMarkers(self, flowline):

        # Add first marker. This needs to be peeled because the for loop
        # connects the markers backwards
        self.imageItemContainer.currentWidget().addItem(flowline[0].getCross()[0])
        self.imageItemContainer.currentWidget().addItem(flowline[0].getCross()[1])

        for i in range(1, len(flowline)):
            self.imageItemContainer.currentWidget().addItem(flowline[i].getCross()[0])
            self.imageItemContainer.currentWidget().addItem(flowline[i].getCross()[1])

            xValuesOfMarkers = [flowline[i - 1].cx, flowline[i].cx]
            yValuesOfMarkers = [flowline[i - 1].cy, flowline[i].cy]

            # Create lines from each marker
            flowline[i].setLine(
                pg.PlotDataItem(xValuesOfMarkers, yValuesOfMarkers, connect='all', pen=skinnyBlackPlotPen), 0)
            flowline[i - 1].setLine(flowline[i].lines[0], 1)

            self.imageItemContainer.currentWidget().addItem(flowline[i].lines[0])

    '''
    Function: displayMarkerVariables
    Argument list: None
    Purpose: Displays the marker variables of the marker selected
    Return types, values: None
    Dependencies: Marker to be selected
    Creator: James Stauder
    Date created: 2/25/18
    Last edited: 2/25/18
    '''

    def displayMarkerVariables(self):
        self.textOut.clear()
        selectedMarkerX = self.whichMarkerSelected.dx
        selectedMarkerY = self.whichMarkerSelected.dy

        self.textOut.append(str((self.whichMarkerSelected.dx, self.whichMarkerSelected.dy)))

        for x in self.maps:
            stringOut = str(self.datasetDict[x.lower()].getInterpolatedValue(selectedMarkerX, selectedMarkerY))
            self.textOut.append(x + ": " + stringOut[2:-2])

    '''
    Function: createIntegrator
    Argument list: Nones
    Purpose: Create integrator class. This will allow us to integrate up the ice flow
    Return types, values: None
    Dependencies: None
    Creator: James Stauder
    Date created: 2/5/18
    Last edited: 2/5/18
    '''

    # TODO: Does this have to be tied to mw? Can this be changed in some way?
    def createIntegrator(self):
        dataFile = h5py.File(dataFileName, 'r')
        vxData = dataFile['Velocity']['VX500'][:]
        vyData = dataFile['Velocity']['VY500'][:]

        vx = Dataset('VX',vxData)
        vy = Dataset('VY',vyData)
        self.flowIntegrator = FlowIntegrator(vx, vy)
        dataFile.close()


    def runModel(self):
        m = ModelGUI(self)

    def reset(self):
        del self.flowlines[:]
        del self.flowlineMarkers[:]
        for x in self.datasetDict:
            self.datasetDict[x].pathData = None
        self.runModelButton.setEnabled(False)
        self.spatialResolutionLineEdit.setReadOnly(False)
        self.distanceLineEdit.setReadOnly(False)
        self.rosieButton.setEnabled(False)
        self.upButton.setEnabled(True)
        self.downButton.setEnabled(True)

    '''
    Function: connectButtons
    Argument list: None
    Purpose: connect the buttons of the gui to various functions
    Return types, values: None
    Dependencies: None
    Creator: James Stauder
    Date created: 2/5/18
    Last edited: 2/5/18
    '''

    def connectButtons(self):
        self.mapList.currentIndexChanged.connect(self.changeMap)
        self.instructionButton.clicked.connect(self.showInstructions)
        self.velocityWidthButton.clicked.connect(self.calcVelocityWidth)
        self.runModelButton.clicked.connect(self.runModel)
        self.resetButton.clicked.connect(self.reset)
        self.latLongButton.clicked.connect(self.markLatLong)
        self.rosieButton.clicked.connect(self.rosie)
        self.latLongButton2.clicked.connect(self.markLatLong2)

    def showInstructions(self):
        Instructions(self)


    def rosie(self):
        dataValues = {}
        xValues = []
        yValues = []
        for dataType in self.datasetDict:
            tempDataName = dataType
            tempDataValues = []
            for point in self.flowlines[0]:
                tempDataValues.append(self.datasetDict[dataType].getInterpolatedValue(point[0], point[1])[0][0])
            dataValues[tempDataName] = tempDataValues

        f = h5py.File(str(self.profileLineEdit.text()), 'w')

        for point in self.flowlines[0]:
            xValues.append(point[0])
            yValues.append(point[1])
        for i in dataValues:
            f.create_dataset(i, data=dataValues[i])
        f.create_dataset('xValues', data = xValues)
        f.create_dataset('yValues', data = yValues)


    def markLatLong(self):

        if (len(self.flowlines) < 2):
            self.rosieButton.setEnabled(True)
            self.spatialResolutionLineEdit.setReadOnly(True)
            self.distanceLineEdit.setReadOnly(True)
            self.flowlineDistance = int(self.distanceLineEdit.text()) * 1000
            self.lengthOfFlowline = int(self.flowlineDistance / float(self.spatialResolutionLineEdit.text()))

            dx, dy = self.translateLatLong(
                float(self.latLineEdit.text()),
                float(self.longLineEdit.text())
            )

            # Create new flowline
            newFlowline = []
            for x in range(0, self.lengthOfFlowline):
                newFlowline.append(None)
            newFlowline[0] = [dx, dy]

            newFlowline = self.flowIntegrator.integrate(dx, dy, newFlowline, 0,
                                                        float(self.spatialResolutionLineEdit.text()))

            if None in newFlowline:
                print "Integration Error. Try Again"
                return

            # Create a flowline of markers spaced out based on the IntegratorPerMarker
            newFlowlineMarkers = newFlowline[::self.integratorPerMarker]

            for i in range(len(newFlowlineMarkers)):
                dx = newFlowlineMarkers[i][0]
                dy = newFlowlineMarkers[i][1]
                cx, cy = colorCoord(dx, dy)
                newFlowlineMarkers[i] = Marker(cx, cy, dx, dy, self.imageItemContainer.currentWidget())

            self.displayMarkers(newFlowlineMarkers)
            self.flowlines.append(newFlowline)
            self.flowlineMarkers.append(newFlowlineMarkers)

    def markLatLong2(self):

        dx, dy = self.translateLatLong(
            float(self.latLineEdit2.text()),
            float(self.longLineEdit2.text())
        )

        cx,cy = colorCoord(dx,dy)
        newSquare = Square(cx, cy, dx, dy, self.imageItemContainer.currentWidget())

        self.imageItemContainer.currentWidget().addItem(newSquare.getCross()[0])
        self.imageItemContainer.currentWidget().addItem(newSquare.getCross()[1])
        self.imageItemContainer.currentWidget().addItem(newSquare.getCross()[2])
        self.imageItemContainer.currentWidget().addItem(newSquare.getCross()[3])


    def translateLatLong(self, lat, long):
        proj = Proj(init = 'epsg:3413')
        return proj(long, lat)
