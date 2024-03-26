from ErrorChecker import  ErrorChecker
from Binary import Binary
from signals import *


class ChecksumChecker(ErrorChecker):

    def __int__(self):
        pass

    def get_header(self):
        return SOH

    def get_error_detecting_code(self, msg_arr):
        msg_sum = 0
        for msg in msg_arr:
            msg_sum += msg.get_int()
        msg_sum = msg_sum % 256
        new_checksum = Binary()
        new_checksum.set_bytes(msg_sum.to_bytes(1, "big"))
        return new_checksum


