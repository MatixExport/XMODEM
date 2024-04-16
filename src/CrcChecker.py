
from crc import Calculator, Crc16
from ErrorChecker import ErrorChecker
from Binary import Binary
from signals import *


class CrcChecker(ErrorChecker):

    def get_header(self):
        return SOH

    def __int__(self):
        self.ufo = 2

    def get_error_detecting_code(self, msg_arr):
        calculator = Calculator(Crc16.CCITT)

        new_crc = Binary()
        data = bytes([msg.get_int() for msg in msg_arr])
        new_crc.set_bytes(calculator.checksum(data).to_bytes(2, "big"))
        return new_crc

    def read_checksum(self, msg_arr):
        return bytearray([int.from_bytes(msg_arr[-2]), int.from_bytes(msg_arr[-1])])

