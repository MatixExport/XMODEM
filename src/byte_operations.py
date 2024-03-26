from Binary import Binary
from Packet import Packet


def int_to_bit_string(int):
    return "{0:b}".format(int)


def byte_string_to_binary_arr(byte_string):
    binary_arr = []
    for byte in byte_string:
        binary = Binary()
        binary.set_value(byte)
        binary_arr.append(binary)
    return binary_arr


def binary_arr_to_byte_string(binary_arr):
    byte_string = bytearray()
    for binary in binary_arr:
        byte_string.append(binary.value)
    return byte_string


def byte_string_to_bytes(byte_string):
    return [byte.to_bytes(1, "big") for byte in byte_string]


def bytes_to_byte_string(bytes):
    byar = bytearray()
    for byte in bytes:
        byar.append(int.from_bytes(byte))
    return byar


def read_file(filename):
    file_packets = []
    try:
        file = open(filename, 'br')
        while read_bytes := file.read(128):
            file_packets.append(read_bytes)
        file.close()
    except IOError as e:
        print(e)
    return file_packets


def write_file(filename, data_arr):
    try:
        file = open(filename, 'bw')
        for block in data_arr:
            file.write(block)
        file.close()
    except IOError as e:
        print(e)


def add_padding(data):
    index = len(data) - 1
    padding = 128 - len(data[index])

    if padding == 0:
        data.append([])
        index += 1
        padding = 128

    for i in range(padding):
        binary = Binary()
        binary.set_value(padding)
        data[index].append(binary)

    return data


def remove_padding(data):
    padding = data[-1][-1].value
    if padding == 128:
        return data[:-1]
    data[-1] = data[-1][:(len(data[-1]) - padding)]
    return data


def pack(data_arr):
    packets = []
    for i in range(len(data_arr)):
        pak = Packet(i)
        pak.set_binary_content(data_arr[i])
        packets.append(pak)
    return packets


def unpack(packets):
    return [packet.get_binary_content() for packet in packets]
