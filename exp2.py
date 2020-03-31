import sys
import time

from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QMainWindow, QVBoxLayout, QSplashScreen)

import keyring
verification_url = "https://attendancekeeper.net/verifydevice.php?license_code="


class Splash(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap('keeper.png')
        splash = self(pixmap)
        splash.setStyleSheet("background: red")
        splash.show()

        

    def check_password(self):

        license_code = self.lineEdit_username.text()
        self.doRequest(license_code)

    def doRequest(self, license_code):
        print("Request started")

        req = QtNetwork.QNetworkRequest(QUrl(verification_url + license_code))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            response = str(bytes_string, 'utf-8')
            if response == "error":
                showMessage("Invalid licence code! Please contact with support", QMessageBox.Warning)
            else:
                key



        else:
            showMessage("Couldn't connect activation server. Try again", QMessageBox.Critical)
    #
    # if self.lineEdit_username.text() == 'a' and self.lineEdit_password.text() == '000':
    #     self.browserWindow.loadAll("https://attendancekeeper.net/westacebd/")
    #     self.browserWindow.show()
    #     self.hide()
    # else:
    #     msg.setText('Incorrect Password')
    #     msg.exec_()


def showMessage(msgText, msg_icon):
    msg = QMessageBox()
    msg.setText(msgText)
    msg.setIcon(msg_icon)
    msg.exec()


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


class BrowserWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BrowserWindow, self).__init__(parent)
        self.setWindowTitle("Attendance Keeper - Westace")
        self.view = QWebEngineView(self)

        self.setCentralWidget(self.view)
        self.setFixedSize(750, 650)

        self.page = WebEnginePage()

        self.frameGm = self.frameGeometry()
        self.screen = app.desktop().screenNumber(app.desktop().cursor().pos())
        self.centerPoint = app.desktop().screenGeometry(self.screen).center()
        self.frameGm.moveCenter(self.centerPoint)
        self.move(self.frameGm.topLeft())

    def loadAll(self, url):
        self.view.setPage(self.page)
        self.view.load(QUrl(url))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
