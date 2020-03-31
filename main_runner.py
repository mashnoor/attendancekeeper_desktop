from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QSplashScreen, QDialog, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
import time


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):

        QWebEnginePage.__init__(self, *args, **kwargs)
        self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)

    def onFeaturePermissionRequested(self, url, feature):
        if feature in (QWebEnginePage.MediaAudioCapture,
                       QWebEnginePage.MediaVideoCapture,
                       QWebEnginePage.MediaAudioVideoCapture):
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)


def showSplash():
    # pixmap = QPixmap('keeper.png')
    # splash = QSplashScreen(pixmap)
    # splash.setStyleSheet("background: red")
    # splash.show()
    #
    # time.sleep(2)
    # splash.close()

    w = QWidget()
    w.resize(300, 300)
    w.setWindowTitle('Guru99')

    label = QLabel(w)
    label.setText("Behold the Guru, Guru99")
    label.move(100, 130)
    label.show()

    btn = QPushButton(w)
    btn.setText('Beheld')
    btn.move(110, 150)
    btn.show()
    w.show()


app = QApplication([])

win = QMainWindow()

showSplash()
win.setWindowTitle("Attendance Keeper - Westace")
view = QWebEngineView(win)

win.setCentralWidget(view)
win.setFixedSize(750, 650)

page = WebEnginePage()

view.setPage(page)
view.load(QUrl("https://attendancekeeper.net/westacebd/clock"))

frameGm = win.frameGeometry()
screen = app.desktop().screenNumber(app.desktop().cursor().pos())
centerPoint = app.desktop().screenGeometry(screen).center()
frameGm.moveCenter(centerPoint)
win.move(frameGm.topLeft())
win.show()


app.exec_()
