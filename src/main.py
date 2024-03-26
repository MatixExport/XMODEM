from connection import *
from byte_operations import *
from byte_operations import read_file, byte_string_to_binary_arr, package_filedata
from connection import xmodem_transmit_file, xmodem_read_file
from Packet import Packet
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file that will be processed')
    parser.add_argument('COM_port_number', help='COM port number', type=int)
    parser.add_argument('-t', '--transmit',
                        action='store_true', help="transmit the selected file")
    parser.add_argument('-c', '--crc',
                        action='store_true', help="use crc instead of checksum")
    args = parser.parse_args()

    com_port_name = "COM" + str(args.COM_port_number)
    if args.transmit:
        packets = read_file(args.file)
        packets = [byte_string_to_binary_arr(packet) for packet in packets]
        packets = package_filedata(packets)
        for i in range(len(packets)):
            pak = Packet(i)
            pak.set_binary_content(packets[i])
            packets[i] = pak
        xmodem_transmit_file(com_port_name, packets)
    else:
        packets = xmodem_read_file(com_port_name, args.crc)
        byte_arr = []
        for packet in packets:
            byte_arr.extend(packet.get_byte_content())
        filedata = byte_arr_to_byte_string(byte_arr)
        filedata = unpackage_filedata(filedata)
        file = open(args.file, 'bw')
        file.write(filedata)
        file.close()

