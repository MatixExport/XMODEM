from Message import Message
from byte_operations import int_to_bit_string


class Packet:

    def __init__(self, _blk):
        self.content = []
        self.blk = _blk

    def add_byte(self, byte):
        if len(self.content) < 128:
            msg = Message()
            msg.set_bytes(byte)
            self.content.append(msg)
            return True
        return False

    def set_content(self, byte_arr):
        for byte in byte_arr:
            self.add_byte(byte)

    def __str__(self):
        output = ""
        for msg in self.content:
            output += msg.get_string()
        output += int_to_bit_string(self.blk) + int_to_bit_string(255 - self.blk)
        return output




