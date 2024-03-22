import signals
from Binary import Binary
from byte_operations import int_to_bit_string
from src.ErrorCheckers.CrcChecker import CrcChecker
from src.ErrorCheckers.ChecksumChecker import ChecksumChecker


class Packet:

    def __init__(self, _blk):
        self.content = []
        self.blk = _blk
        self.blk_check = None
        self.checksum = Binary()
        self.error_checker = ChecksumChecker()

    def add_byte(self, byte):
        if len(self.content) < 128:
            msg = Binary()
            msg.set_bytes(byte)
            self.content.append(msg)
            return True
        return False

    def set_crc_mode(self, is_crc):
        if is_crc:
            self.error_checker = CrcChecker()
            return
        self.error_checker = ChecksumChecker()

    def set_content(self, byte_arr):
        for byte in byte_arr:
            self.add_byte(byte)

    def get_byte_content(self):
        return [i.get_bytes() for i in self.content]

    def get_bytes(self):
        byte_arr = [self.blk.to_bytes(1, "big"), (255 - self.blk).to_bytes(1, "big")]

        for msg in self.content:
            byte_arr.append(
                msg.get_bytes()
            )

        byte_arr.insert(0, self.error_checker.get_header().to_bytes(1, 'big'))
        byte_arr.append(self.error_checker.get_error_detecting_code(self.content).get_bytes())
        return byte_arr

    def from_bytes(self, data):
        self.blk = int.from_bytes(data[1], 'big')
        self.blk_check = int.from_bytes(data[2], 'big')

        for i in range(3, 131):
            msg = Binary()
            msg.set_bytes(data[i])
            self.content.append(msg)

        self.set_crc_mode(int.from_bytes(data[0], byteorder='big') == signals.CRC_MODE)
        self.checksum.set_bytes(data[-1])
        return self

    def is_valid(self):
        if self.blk + self.blk_check != 255:
            return False
        if not self.error_checker.validate_error_detecting_code(self.content, self.checksum):
            return False
        return True

    def __str__(self):
        output = ""
        for msg in self.content:
            output += msg.get_string()
        output += int_to_bit_string(self.blk) + int_to_bit_string(255 - self.blk)
        return output
