import time
from signals import *
from Packet import Packet
from byte_operations import bytes_to_byte_string, byte_string_to_bytes
import serial


def signal_to_byte(_signal):
    return _signal.to_bytes()


def initialize_port(port_name):
    ser = serial.Serial()
    ser.port = port_name
    ser.timeout = 12
    ser.baudrate = 19200
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    return ser


def initialize_read_connection(port, crc_mode):
    init_time = time.time()
    last_request_time = 0
    signal_to_send = CRC_MODE if crc_mode else NAK

    while time.time() - init_time <= 60:
        if time.time() - last_request_time >= 10:
            print("Sending NAK or C to transmitter")
            port.write(signal_to_byte(signal_to_send))
            last_request_time = time.time()
        if port.in_waiting:
            return True
    print("Timeout, reader is unable to connect")
    return False


def start_read_file(port):
    packages = []
    read_msg = None
    while read_msg != signal_to_byte(EOT):
        if port.in_waiting:
            if port.in_waiting < 10:
                read_msg = port.read(port.in_waiting)
                print("Recived Signal = ", read_msg)
                continue
            print("Reading a Packet")
            read_msg = port.read(port.in_waiting)
            pack = Packet.from_bytes(byte_string_to_bytes(read_msg))
            if pack.is_valid():
                packages.append(pack)
                port.write(signal_to_byte(ACK))
            else:
                port.write(signal_to_byte(NAK))
    return packages


def xmodem_read_file(port_name, crc_mode=False):
    serial_port = initialize_port(port_name)
    serial_port.open()
    initialize_read_connection(serial_port, crc_mode)
    packages = start_read_file(serial_port)
    serial_port.close()
    return packages


def wait_for_signal(port, timeout=60):
    init_time = time.time()
    while time.time() - init_time <= timeout:
        if port.in_waiting:
            return port.read(1)
    return None


def send_EOT(port, tries=2):
    while tries > 0:
        port.write(signal_to_byte(EOT))
        print("Sending EOT")
        signal = wait_for_signal(port, 10)
        if signal == signal_to_byte(ACK):
            print("Received ACK to EOT")
            return True
        tries -= 1
        print("ACK not received, resending EOT")
    print("Retries limit for EOT reached, ending transmission without ACK")
    return False


def send_packet(port, packet):
    port.write(bytes_to_byte_string(packet.get_bytes()))
    signal = wait_for_signal(port)
    if signal == signal_to_byte(NAK):
        print("Invalid Packet was received, resending last Packet")
        return send_packet(port, packet)
    if signal == signal_to_byte(CAN):
        print("CAN received, ending connection")
        return False
    return True


def xmodem_transmit_file(port_name, packets):
    serial_port = initialize_port(port_name)
    serial_port.open()
    crc_mode = False
    while True:
        print("Transmitter is waiting for connection")
        signal = wait_for_signal(serial_port)
        print("Recived Connection")

        if signal == signal_to_byte(NAK):
            crc_mode = False
        elif signal == signal_to_byte(CRC_MODE):
            crc_mode = True
        else:
            print("Invalid Header, Restarting connection")
            continue
        print("Transmitter Connected")
        i = 0
        # wysyłanie pakietów
        while i < len(packets):
            print("Transmitter is sending packet", i)
            if crc_mode:
                packets[i].set_crc_mode(True)
            if not send_packet(serial_port, packets[i]):
                exit(0)
            i += 1
        print("Ending Connection")
        send_EOT(serial_port)
