import signals
from Binary import Binary
from byte_operations import int_to_bit_string
from crc import calculate_xmodem_crc


# nie podoba mi się ten crc_mode i te
# ify z tego wynikające
# jeszcze nie wiem jak to rozdzielę
# ale tak nie zostanie
# może rozdzielę to na 2 klasy
class Packet:

    def __init__(self, _blk):
        self.content = []
        self.blk = _blk
        self.blk_check = None
        self.checksum = Binary()
        self.crc_mode = False

    def add_byte(self, byte):
        if len(self.content) < 128:
            msg = Binary()
            msg.set_bytes(byte)
            self.content.append(msg)
            return True
        return False

    def set_crc_mode(self, is_crc):
        self.crc_mode = is_crc

    def calculate_checksum(self):
        msg_sum = 0
        for msg in self.content:
            msg_sum += msg.get_int()
        msg_sum = msg_sum % 256
        self.checksum.set_bytes(msg_sum.to_bytes(1, "big"))
        return self.checksum

    def calculate_crc(self):
        crc = calculate_xmodem_crc(self.content)
        self.checksum.set_bytes(crc.to_bytes(2, "big"))
        return self.checksum

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

        if self.crc_mode:
            self.calculate_crc()
            byte_arr.insert(0, signals.CRC_MODE.to_bytes(1, 'big'))

        else:
            self.calculate_checksum()
            byte_arr.insert(0, signals.SOH.to_bytes(1, 'big'))

        byte_arr.append(self.checksum.get_bytes())
        return byte_arr

    def from_bytes(self, data):
        self.blk = int.from_bytes(data[1], 'big')
        self.blk_check = int.from_bytes(data[2], 'big')

        for i in range(3, 131):
            msg = Binary()
            msg.set_bytes(data[i])
            self.content.append(msg)

        _checksum = Binary()
        if int.from_bytes(data[0], byteorder='big') == signals.CRC_MODE:
            self.crc_mode = True

        _checksum.set_bytes(data[-1])
        self.checksum = _checksum
        return self

    def _is_crc_valid(self):
        return self.checksum.value == self.calculate_crc().value

    def _is_checksum_valid(self):
        return self.checksum.value == self.calculate_checksum().value

    def is_valid(self):
        if self.blk + self.blk_check != 255:
            return False
        if self.crc_mode:
            if not self._is_crc_valid():
                return False
        else:
            if not self._is_checksum_valid():
                return False
        return True

    def __str__(self):
        output = ""
        for msg in self.content:
            output += msg.get_string()
        output += int_to_bit_string(self.blk) + int_to_bit_string(255 - self.blk)
        return output
