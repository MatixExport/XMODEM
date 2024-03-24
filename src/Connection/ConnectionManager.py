import serial


class ConnectionManager:

    def __init__(self, port_name,crc_mode=False):
        self.continue_reading = None
        self.port_name = port_name
        self.serial = None
        self.continue_reading = False
        self.last_send_msg = None
        self.initialize_port()
        self.crc_mode = crc_mode

    def initialize_port(self):
        ser = serial.Serial()
        ser.port = self.port_name
        ser.timeout = 12
        ser.baudrate = 19200
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.bytesize = serial.EIGHTBITS
        self.serial = ser

    def is_reading(self):
        return self.continue_reading

    def stop_reading(self):
        self.continue_reading = False

    def send_serial(self,msg):
        if not self.serial.is_open:
            self.serial.open()
            self.serial.write(msg)
            self.serial.close()
            return
        self.serial.write(msg)

    def read_serial(self):
        self.continue_reading = True
        if not self.serial.is_open:
            self.serial.open()
        while self.continue_reading:
            msg = self.serial.read(132)
            self.on_receive_msg(msg)
        self.serial.close()

    def on_receive_msg(self,received_msg):
        pass
