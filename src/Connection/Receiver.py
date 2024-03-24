from ConnectionManager import ConnectionManager
from serial import Serial
from src.signals import *


class Receiver(ConnectionManager):

    def start_connection(self):
        self.serial.open()
        self.send_serial(A)
