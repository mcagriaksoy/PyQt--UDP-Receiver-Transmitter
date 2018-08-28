__author__ = 'Mehmet Cagri Aksoy - github.com/mcagriaksoy'

import socket
import sys
from PyQt5.QtWidgets import QApplication, QMenu, QMainWindow
from PyQt5.uic import loadUi

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
# print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)


class qt(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('receiver.ui', self)

    def on_pushButton_clicked(self):
        data, address = sock.recvfrom(4096)
        print('received {} bytes from {}'.format(len(data), address))
        print(data.decode('utf-8'))

        self.textEdit.setText(data.decode('utf-8'))


def run():
    app = QApplication(sys.argv)
    widget = qt()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
