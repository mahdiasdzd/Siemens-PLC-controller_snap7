import snap7
import struct

class PLCCommunication:
    def __init__(self, ip_address, rack, slot):
        self.plc = snap7.client.Client()
        self.plc.connect(ip_address, rack, slot)

    def write_bool(self, db_number, start_offset, bit_offset, value):
        reading = self.plc.db_read(db_number, start_offset, 1)  # Read 1 byte
        snap7.util.set_bool(reading, 0, bit_offset, value)  # Set the boolean value
        self.plc.db_write(db_number, start_offset, reading)  # Write the modified byte

    def read_bool(self, db_number, start_offset, bit_offset):
        reading = self.plc.db_read(db_number, start_offset, 1)  # Read 1 byte
        a = snap7.util.get_bool(reading, 0, bit_offset)
        print(f'DB Number: {db_number} Start Offset: {start_offset} Bit Offset: {bit_offset} Value: {a}')

    def write_timer(self, db_number, start_offset, bit_offset, timer_value):
        if self.plc.get_connected():
            existing_data = self.plc.db_read(db_number, start_offset, 8)  # Assuming the timer is 8 bytes long
            packed_timer_value = struct.pack('>I', int(timer_value * 1000))  # Assuming timer is in milliseconds
            existing_data = existing_data[:4] + packed_timer_value + existing_data[8:]
            self.plc.db_write(db_number, start_offset, existing_data)
            print(f"Write successful. DB: {db_number} Start Offset: {start_offset} Bit Offset: {bit_offset} Value: {timer_value} seconds")
        else:
            print("Connection to PLC failed.")

    def read_timer(self, db_number, start_offset, bit_offset):
        if self.plc.get_connected():
            data_block = self.plc.db_read(db_number, start_offset, 8)  # Assuming the timer is 8 bytes long
            packed_timer_value = data_block[:4]
            timer_value = struct.unpack('>I', packed_timer_value)[0] / 1000.0  # Convert back to seconds
            print(f"Read successful. DB: {db_number} Start Offset: {start_offset} Bit Offset: {bit_offset} Value: {timer_value} seconds")
        else:
            print("Connection to PLC failed.")

    def get_cpu_state(self):
        return self.plc.get_cpu_state()

    def disconnect(self):
        self.plc.disconnect()


'''ip_address = '192.168.0.1'
rack = 0
slot = 1

db_number = 46
start_offset = 0
bit_offset = 0

value = 0
timer_value = 20

plc_communication = PLCCommunication(ip_address = '192.168.0.1', rack = 0, slot = 1)

#print(plc_communication.get_cpu_state())


#plc_communication.read_bool(db_number, start_offset, bit_offset)
#plc_communication.write_bool(db_number, start_offset, bit_offset, value)
#plc_communication.read_bool(db_number, start_offset, bit_offset)

#plc_communication.read_timer(db_number, start_offset, bit_offset)
#plc_communication.write_timer(db_number, start_offset, bit_offset, timer_value)
#plc_communication.read_timer(db_number, start_offset, bit_offset)

#plc_communication.disconnect()'''
