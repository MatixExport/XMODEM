from Binary import Binary


def int_to_bit_string(int):
    return "{0:b}".format(int)

def byte_string_to_binary_arr(byte_string):
    binary_arr = []
    for byte in byte_string:
        binary = Binary()
        binary.set_value(byte)
        binary_arr.append(binary)
    return binary_arr

def byte_string_to_bytes(byte_string):
    return [byte.to_bytes(1,"big") for byte in byte_string]

def byte_arr_to_byte_string(bytes):
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


def package_filedata(data):
    index = len(data) - 1
    padding = 128 - len(data[index])

    if padding == 0:
        index += 1
        padding = 128

    for i in range(padding):
        binary = Binary()
        binary.set_value(padding)
        data[index].append(binary)

    return data

def unpackage_filedata(data):
    padding = data[-1]
    data = data[:len(data) - padding]
    return data
