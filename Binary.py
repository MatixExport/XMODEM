from math import ceil


class Binary:

    def __init__(self):
        self.value = 0
        self.number_of_bits = 0

    def append(self, bit):
        self.number_of_bits += 1
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
        self.number_of_bits = len(bytes) * 8 - 1
        self.value = int.from_bytes(bytes, 'big')

    def get_bytes(self):
        return self.value.to_bytes(ceil(self.number_of_bits / 8), 'big')

    def get_bytes_as_array(self):
        num_of_bytes = ceil(self.number_of_bits / 8)
        byte_arr = []
        for i in range(num_of_bytes):
            print(i)
            byte_arr.append(
                ((self.value >> i*8) & 0x00FF).to_bytes(1,'big')
            )
        return byte_arr

    def get_int(self):
        return self.value

    def get_string(self):
        tab = ['0', '1']
        output = ""
        for i in range(self.number_of_bits, -1, -1):
            output += tab[self.get_bit_at_index(i)]
        return output

    def __int__(self):
        return self.value
