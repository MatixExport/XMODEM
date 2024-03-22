from src.ErrorCheckers.ErrorChecker import ErrorChecker
from src.crc import calculate_xmodem_crc
from src.Binary import Binary
from src.signals import *


class CrcChecker(ErrorChecker):

    def get_header(self):
        return CRC_MODE

    def __int__(self):
        self.ufo = 2

    def get_error_detecting_code(self, msg_arr):
        crc = calculate_xmodem_crc(msg_arr)
        new_crc = Binary()
        new_crc.set_bytes(crc.to_bytes(2, "big"))
        return new_crc


