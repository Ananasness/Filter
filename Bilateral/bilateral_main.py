from PyQt5 import QtGui, QtWidgets, uic, QtCore
import sys
from bilateral import bilateral

app = QtWidgets.QApplication(sys.argv)
defaultSigma = 100
defaultRadius = 3

class MainWindow (QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('bil.ui', self)
        self.pushButtonLoad.clicked.connect(self.load_image)
        self.pushButtonStart.clicked.connect(self.start)


    def load_image(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "./", "Images (*.png *.jpg)") #, str_filter=str("Image (*.jpg)"))#, str_caption="Load your image")
        self.image = QtGui.QImage(file_name[0])
        self.labelSource.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.labelSource.setScaledContents(True)

    def start(self):
        sigma = defaultSigma
        radius = defaultRadius
        try:
            sigma = int(self.lineEditSigma.text())
            radius = int(self.lineEditRadius.text())
        except ValueError:
            print("Invalid value")
            return
        image_bil = bilateral(self.image, sigma, radius)
        self.labelBilateral.setPixmap(QtGui.QPixmap.fromImage(image_bil))
        self.labelBilateral.setScaledContents(True)


mw = MainWindow()
mw.show()
app.exec_()
