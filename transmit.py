__author__ = 'Mehmet Cagri Aksoy - github.com/mcagriaksoy'

import socket
import sys

from PyQt5.QtWidgets import QApplication, QMenu, QMainWindow
from PyQt5.uic import loadUi

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)



class qt(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('transmit.ui', self)


    def on_pushButton_clicked(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.001
            self.progressBar.setValue(self.completed)

            # Send data
        # print('sending {!r}'.format(message))
        mesaj=self.textEdit.toPlainText().encode('utf-8')
        sock.sendto(mesaj, server_address)

        # Receive response
        # print('waiting to receive')
        # data, server = sock.recvfrom(4096)
        # print('received {!r}'.format(data))

    def on_pushButton_2_clicked(self):
        sock.close()
        self.textEdit.setText("Soket Kapatıldı...")


def run():
    app = QApplication(sys.argv)
    widget = qt()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
