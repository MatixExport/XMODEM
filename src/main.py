from connection import *
from byte_operations import *
from byte_operations import read_file, byte_string_to_binary_arr, add_padding,pack
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
        filedata = read_file(args.file)
        filedata = [byte_string_to_binary_arr(block) for block in filedata]
        packets = add_padding(filedata)
        packets = pack(packets)
        xmodem_transmit_file(com_port_name, packets)
    else:
        packets = xmodem_read_file(com_port_name, args.crc)
        filedata = unpack(packets)
        filedata = remove_padding(filedata)
        filedata = [binary_arr_to_byte_string(binary_arr) for binary_arr in filedata]
        write_file(args.file, filedata)

