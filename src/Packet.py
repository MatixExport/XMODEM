import signals
from Binary import Binary
from CrcChecker import CrcChecker
from ChecksumChecker import ChecksumChecker


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

    def set_binary_content(self, binary_arr):
        for binary in binary_arr:
            self.content.append(binary)

    def get_byte_content(self):
        return [i.get_bytes() for i in self.content]

    def get_binary_content(self):
        return self.content

    def get_bytes(self):
        byte_arr = [self.blk.to_bytes(1, "big"), (255 - self.blk).to_bytes(1, "big")]

        for msg in self.content:
            byte_arr.append(
                msg.get_bytes()
            )

        byte_arr.insert(0, self.error_checker.get_header().to_bytes(1, 'big'))
        byte_arr.extend(reversed(self.error_checker.get_error_detecting_code(self.content).get_bytes_as_array()))
        # print("Just After extension",byte_arr)
        return byte_arr

    @staticmethod
    def from_bytes(data):
        packet = Packet(int.from_bytes(data[1], 'big'))
        packet.blk_check = int.from_bytes(data[2], 'big')

        for i in range(3, 131):
            msg = Binary()
            msg.set_bytes(data[i])
            packet.content.append(msg)

        # packet.set_crc_mode(data[0] == signals.CRC_MODE.to_bytes(1, 'big'))
        packet.checksum.set_bytes(packet.error_checker.read_checksum(data))
        return packet

    def is_valid(self):
        if self.blk + self.blk_check != 255:
            return False
        if not self.error_checker.validate_error_detecting_code(self.content, self.checksum):
            return False
        return True
