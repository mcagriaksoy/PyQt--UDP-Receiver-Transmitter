__author__ = 'Mehmet Cagri Aksoy - github.com/mcagriaksoy'

import socket
import sys
import time

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMenu, QMainWindow
from PyQt5.uic import loadUi

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print('starting up on {} port {}'.format(*server_address))
server_address = ('255.255.255.255', 37020)
sock.bind(server_address)



class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    @pyqtSlot()
    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

    def work(self):
        while self.working:
            data, address = sock.recvfrom(1024)
            print('received {} bytes from {}'.format(len(data), address))
            # time.sleep(0.05)
            data2 = data.decode('utf-8')
            self.intReady.emit(data2)

        self.finished.emit()


class qt(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('receiver.ui', self)
        self.thread = None
        self.worker = None
        self.pushButton.clicked.connect(self.start_loop)

    def loop_finished(self):
        self.textEdit.setText("Durduruldu!")

    def start_loop(self):
        print("thread is started")
        self.worker = Worker()  # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        self.worker.moveToThread(self.thread)
        # move the worker into the thread, do this first before connecting the signals
        self.thread.started.connect(self.worker.work)
        # begin our worker object's loop when the thread starts running
        self.worker.intReady.connect(self.onintready)
        self.worker.finished.connect(self.loop_finished)  # do something in the gui when the worker loop ends
        self.pushButton_2.clicked.connect(self.stop_loop)  # stop the loop on the stop button click

        self.worker.finished.connect(self.thread.quit)  # tell the thread it's time to stop running
        self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)  # have thread mark itself for deletion
        # make sure those last two are connected to themselves or you will get random crashes
        self.thread.start()

    def onintready(self, data2):
        self.textEdit.append("{}".format(data2))
        print(data2)

    def stop_loop(self):
        self.worker.working = False


def run():
    app = QApplication(sys.argv)
    widget = qt()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
