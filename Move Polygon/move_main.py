from PyQt5 import QtGui, QtWidgets, uic, QtCore
import sys
import random
import numpy as np

app = QtWidgets.QApplication(sys.argv)


class MainWindow (QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('mp.ui', self)

        # scenes initialization
        self.scene_before = QtWidgets.QGraphicsScene(self)
        self.scene_after = QtWidgets.QGraphicsScene(self)
        self.graphicsViewBefore.setScene(self.scene_before)
        self.graphicsViewAfter.setScene(self.scene_after)

        # buttons binding
        self.pushButtonLoad.clicked.connect(self.generate_random_polygon)
        self.pushButtonStart.clicked.connect(self.start)

        #
        self.points = []
        self.polygon = QtWidgets.QGraphicsPolygonItem()
        self.scene_after.addItem(self.polygon)
        self.load_polygon()

    def build_polygon(self, points):
        polygon = QtGui.QPolygonF()
        for point in points:
            polygon.append(QtCore.QPointF(point[0], point[1]))

        return polygon

    def load_polygon(self):
        file = open("input")
        original_polygon = QtGui.QPolygonF()
        self.points.clear()
        for line in file:
            line = line.split(" ")
            self.points.append([100*float(line[0]), 100*float(line[1])])
            point = QtCore.QPointF(100*float(line[0]), 100*float(line[1]))
            original_polygon.append(point)

        # self.polygon = QtWidgets.QGraphicsPolygonItem(original_polygon)
        self.scene_before.addPolygon(original_polygon)
        self.scene_before.update()

    def start(self):
        angle = np.radians(float(self.lineEditAngle.text()))
        dx = float(self.lineEditdx.text())
        dy = float(self.lineEditdy.text())

        arr = np.array(self.points)

        # rotate
        rotate_matrix = np.array([[np.cos(angle), np.sin(angle)],
                                  [-np.sin(angle), np.cos(angle)]])

        for i in range(len(arr)):
            arr[i] = np.dot(rotate_matrix, arr[i])

        # shift
        points = arr + np.array([[dx, dy] for _ in range(len(arr))])

        # update polygon after
        self.polygon.setPolygon(self.build_polygon(points))


    def generate_random_polygon(self):
        n = random.randint(3, 10)
        self.points.clear()
        for i in range(n):
            self.points.append([random.randint(-100, 100), random.randint(-100, 100)])
        self.scene_before.clear()
        self.scene_before.addPolygon(self.build_polygon(self.points))
        self.scene_before.update()



mw = MainWindow()
mw.show()
app.exec_()
