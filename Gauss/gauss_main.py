from PyQt5 import QtGui, QtWidgets, uic, QtCore
import sys
from gauss import gauss_filter

app = QtWidgets.QApplication(sys.argv)


class MainWindow (QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('gauss.ui', self)
        self.pushButtonLoad.clicked.connect(self.load_image)
        self.pushButtonStart.clicked.connect(self.start_gauss)

    def load_image(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/", "Images (*.jpg)")
        self.image = QtGui.QImage(fileName)
        self.labelSource.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.labelSource.setScaledContents(True)

    def start_gauss(self):
        try:
            sigma = int(self.lineEditSigma.text())
        except ValueError:
            print("Invalid sigma value: " + self.lineEditSigma.text())
            return
        image_gauss = gauss_filter(self.image, sigma)
        self.labelGauss.setPixmap(QtGui.QPixmap.fromImage(image_gauss))
        self.labelGauss.setScaledContents(True)

        image_gaussX = gauss_filter(self.image, sigma, der="x")
        self.labelDerX.setPixmap(QtGui.QPixmap.fromImage(image_gaussX))
        self.labelDerX.setScaledContents(True)

        image_gaussY = gauss_filter(self.image, sigma, der="y")

        self.labelDerY.setPixmap(QtGui.QPixmap.fromImage(image_gaussY))
        self.labelDerY.setScaledContents(True)



mw = MainWindow()
mw.show()
app.exec_()
