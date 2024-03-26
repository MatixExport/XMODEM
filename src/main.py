from connection import *
from byte_operations import *

packages = xmodem_read_file("COM3",True)


file = open("halo2",'bw')

byte_arr = []
for packet in packages:
    byte_arr.extend(packet.get_byte_content())
final = byte_arr_to_byte_string(byte_arr)
final = unpackage_filedata(final)
file.write(final)
file.close()





















