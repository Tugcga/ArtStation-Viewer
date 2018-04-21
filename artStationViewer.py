import sys
import requests
import os
import json
from PySide import QtGui, QtCore


def GetDataTitle(data, index):
    d = data[index]
    t = d["title"]

    if "user" in d:
        jUser = d["user"]
        return jUser["first_name"] + " " + jUser["last_name"] + " (" + jUser["username"] + ") - " + t
    else:
        return t


def GetImageName(data, index):
    d = data[index]
    link = d["cover"]["medium_image_url"]
    parts = link.split('/')
    return parts[len(parts) - 1].rsplit("?", 1)[0]


def GetImageLink(data, index):
    rawStr = data[index]["cover"]["medium_image_url"]
    parts = rawStr.rsplit("?", 1)
    # return data[index]["cover"]["medium_image_url"]
    return parts[0]


class viewWindow(QtGui.QMainWindow):
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2 - 40)

    def setStyle(self):
        self.titleLabel.setStyleSheet("QLabel {background-color: #222222; color: #CCC}")
        self.pathLabel.setStyleSheet("QLabel {color: #CCC}")
        self.titleShadow = QtGui.QGraphicsDropShadowEffect(self)
        self.titleShadow.setBlurRadius(8)
        self.titleShadow.setOffset(0, 4)
        self.titleShadow.setColor(QtGui.QColor(24, 24, 24, 128))
        self.titleLabel.setGraphicsEffect(self.titleShadow)

        self.imageShadow = QtGui.QGraphicsDropShadowEffect(self)
        self.imageShadow.setBlurRadius(20)
        self.imageShadow.setOffset(0)
        self.imageShadow.setColor(QtGui.QColor(24, 24, 24, 255))
        self.imageLabel.setGraphicsEffect(self.imageShadow)

        self.setStyleSheet("""QWidget#centralWidget {background-color: #272727}
                                QPushButton { 
                                                background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #222222,
                                                    stop: 1 #222222 );
                                                border: 3;
                                                border-radius: 6px;
                                                color: #CCC;}

                                QPushButton:hover { 
                                                    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #222222,
                                                    stop: 1 #202020); }

                                QPushButton:pressed { 
                                                        background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #202020,
                                                    stop: 1 #222222); }

                                QLineEdit { border: 2px solid #404040;
                                            border-radius: 5px;
                                            background: #404040;
                                            selection-background-color: darkgray;
                                            color: #CCC}

                                QMenuBar {
                                            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                                              stop:0 #404040, stop:1 #353535);}

                                QMenuBar::item {
                                    spacing: 3px;
                                    padding: 1px 4px;
                                    background: transparent;
                                    color: #CCC}

                                QMenuBar::item:selected {
                                    background: #353535;}

                                QMenuBar::item:pressed {
                                    background: #353535;}

                                QStatusBar {
                                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                                              stop:0 #404040, stop:1 #353535);
                                    color: #CCC;}
""")

    def setupUi(self, MainWindow):
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(18)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.titleLabel.setFont(font)
        self.titleLabel.setTextFormat(QtCore.Qt.PlainText)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 10, 0, 5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prevButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prevButton.sizePolicy().hasHeightForWidth())
        self.prevButton.setSizePolicy(sizePolicy)
        self.prevButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.prevButton.setMinimumSize(QtCore.QSize(50, 0))
        self.prevButton.setObjectName("prevButton")

        prevIcon = QtGui.QIcon("icons\\prevIcon.png")
        self.prevButton.setIcon(prevIcon)
        self.prevButton.setIconSize(QtCore.QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.prevButton)
        self.connect(self.prevButton, QtCore.SIGNAL("clicked()"), self.signalToPrevImage)
        self.imageLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.imageLabel)
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.nextButton.setMinimumSize(QtCore.QSize(50, 0))
        self.nextButton.setObjectName("nextButton")
        nextIcon = QtGui.QIcon("icons\\nextIcon.png")
        self.nextButton.setIcon(nextIcon)
        self.nextButton.setIconSize(QtCore.QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.nextButton)
        self.connect(self.nextButton, QtCore.SIGNAL("clicked()"), self.signalToNextImage)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pathLabel = QtGui.QLabel(self.centralwidget)
        self.pathLabel.setText("Save path")
        self.horizontalLayout.addWidget(self.pathLabel)
        self.pathLine = QtGui.QLineEdit(self.centralwidget)
        self.pathLine.setObjectName("pathLine")
        self.pathLine.setText(os.path.dirname(os.path.abspath(__file__)) + "\\saveImages\\")
        self.horizontalLayout.addWidget(self.pathLine)
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setMinimumSize(QtCore.QSize(80, 30))
        self.saveButton.setMaximumSize(QtCore.QSize(80, 30))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Save")
        sIcon = QtGui.QIcon("icons\\saveIcon.png")
        self.saveButton.setIcon(sIcon)
        self.saveButton.setIconSize(QtCore.QSize(20, 20))
        self.connect(self.saveButton, QtCore.SIGNAL("clicked()"), self.signalSave)
        self.horizontalLayout.addWidget(self.saveButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.imageLabel.resize(1024, 768)
        self.resize(1146, 931)

        self.center()

        self.setWindowTitle("ArtStation viewer")
        self.setWindowIcon(QtGui.QIcon('icons\\Icon.png'))

        self.statusBar()

        aClose = QtGui.QAction("Close", self)
        aClose.setStatusTip("Close window")
        aClose.setShortcut("Ctrl+Q")
        self.connect(aClose, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))

        aUpdate = QtGui.QAction("Update", self)
        aUpdate.setShortcut("Ctrl+U")
        aUpdate.setStatusTip("Update connection and load references to images")
        self.connect(aUpdate, QtCore.SIGNAL("triggered()"), self.signalUpdate)

        aSave = QtGui.QAction("Save image", self)
        aSave.setShortcut("Ctrl+S")
        aSave.setStatusTip("Save image")
        self.connect(aSave, QtCore.SIGNAL("triggered()"), self.signalSave)

        menubar = self.menuBar()
        file = menubar.addMenu("File")
        file.addAction(aUpdate)
        file.addAction(aSave)
        file.addAction(aClose)

        self.setStyle()

    def signalUpdate(self):
        self.statusBar().showMessage("Update images data")
        print(self.link % self.dataNumber)
        response = requests.get(self.link % self.dataNumber)
        parsed_json = json.loads(response.text)
        self.data = parsed_json['data']

        self.statusBar().showMessage("Data obtained with key " + str(self.dataNumber))
        self.dataNumber = self.dataNumber + 1
        self.currentImageIndex = 0
        self.maxImagesIndexes = len(self.data)

        self.showImage()

    def signalSave(self):
        folderName = self.pathLine.text()
        if not os.path.exists(folderName):
            os.makedirs(folderName)
        output = open(folderName + GetImageName(self.data, self.currentImageIndex), "wb")
        output.write(self.imageData)
        output.close()

    def signalToNextImage(self):
        if len(self.data) == 0:
            self.signalUpdate()
        if self.currentImageIndex < self.maxImagesIndexes - 1:
            self.currentImageIndex = self.currentImageIndex + 1
        else:
            self.signalUpdate()

        self.imageLabel.clear()
        self.titleLabel.setText("Loading...")
        self.showImage()

    def signalToPrevImage(self):
        if len(self.data) == 0:
            self.signalUpdate()
        if self.currentImageIndex > 0:
            self.currentImageIndex = self.currentImageIndex - 1

        self.imageLabel.clear()
        self.titleLabel.setText("Loading...")
        self.showImage()

    def showImage(self):
        lSize = self.imageLabel.size()
        if lSize.width() < 1024:
            self.imageLabel.resize(1024, lSize.height())
        if lSize.height() < 768:
            self.imageLabel.resize(lSize.width(), 768)

        self.statusBar().showMessage("Page: " + str(self.dataNumber - 1) + ". Image: " + str(self.currentImageIndex + 1) + " (from " + str(self.maxImagesIndexes) + "). Link: " +  GetImageLink(self.data, self.currentImageIndex))

        self.titleLabel.setText(GetDataTitle(self.data, self.currentImageIndex))
        url = self.data[self.currentImageIndex]["cover"]["medium_image_url"]
        self.imageData = requests.get(url).content
        self.pixmap = QtGui.QPixmap()
        self.originalPixMap = QtGui.QPixmap()
        self.originalPixMap.loadFromData(self.imageData)

        self.pixmap = self.originalPixMap.scaled(self.imageLabel.size().width(), self.imageLabel.size().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.imageLabel.setPixmap(self.pixmap)

    def resizeEvent(self, event):

        w = self.originalPixMap.width()
        h = self.originalPixMap.height()

        self.pixmap = self.originalPixMap.scaled(min(self.imageLabel.size().width(), w), min(self.imageLabel.size().height(), h), QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(self.pixmap)

    def __init__(self, k, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.link = ""
        if int(k) == 0:
            self.link = "https://www.artstation.com/projects.json?page=%s&randomize=true"
        else:
            self.link = "https://www.artstation.com/projects.json?page=%s&sorting=trending"
        self.setupUi(self)

        self.dataNumber = 1
        self.signalUpdate()


def main():
    print(sys.argv)
    app = QtGui.QApplication(sys.argv)
    if len(sys.argv) > 1:
        window = viewWindow(sys.argv[1])
    else:
        window = viewWindow(0)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
