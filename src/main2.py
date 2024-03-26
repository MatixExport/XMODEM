from byte_operations import read_file, byte_string_to_binary_arr, package_filedata
from connection import xmodem_transmit_file
from Packet import Packet

#
# data = [i.to_bytes(1,'big') for i in range(128)]
# pack = Packet(1)
# pack.set_crc_mode(True)
# pack.set_content(data)
# # print(pack.calculate_crc().value)
# # for msg in pack.content:
# #     print(msg.value)
#
#
# pack2 = Packet(1)
#
#
# pack2 = Packet.from_bytes(pack2.get_bytes())
# # print(pack2.calculate_crc().value)
# print(pack2.is_valid())

# for msg in pack2.content:
#     print(msg.value)


packets = read_file("halo.txt")
packets = [byte_string_to_binary_arr(packet) for packet in packets]
packets = package_filedata(packets)

for i in range(len(packets)):
    pak = Packet(i)
    pak.set_binary_content(packets[i])
    packets[i] = pak

#
# for packet in packets:
#     for binary in packet.content:
#         print(binary.value)

xmodem_transmit_file('COM4', packets)
