from math import ceil


class Message:

    def __init__(self):
        self.value = 0
        self.occupied_index = 0

    def append(self, bit):
        self.occupied_index += 1
        self.value = self.value << 1
        self.set(0, bit)

    def set(self, index, bit):
        if bit == 0 or bit == '0':
            self.value = self.value & ~(1 << index)
        else:
            self.value = self.value | 1 << index

    def get_bit_at_index(self, index):
        return (self.value >> index) & 1

    def set_bytes(self, bytes):
        self.occupied_index = len(bytes) * 8 - 1
        self.value = int.from_bytes(bytes)

    def fill_to_full_bytes(self):
        for i in range(8 - ((self.occupied_index+1) % 8)):
            self.append(0)

    def get_bytes(self):
        return self.value.to_bytes(ceil(self.occupied_index / 8))

    def get_string(self):
        tab = ['0', '1']
        output = ""
        for i in range(self.occupied_index, -1, -1):
            output += tab[self.get_bit_at_index(i)]
        return output

