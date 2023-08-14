import serial

# Replace with the correct port name for your system
# On Windows, it might be 'COM3' or 'COM4'
# On Linux or Mac, it might be '/dev/ttyUSB0' or similar
port = '/dev/cu.usbmodem1301'

ser = serial.Serial(port, 9600, timeout=1)

try:
    while True:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        if line:  # If line is not empty
            axis_x, axis_y, sw_p = map(int, line.split(' '))     # Split the line by spaces
            print(f"AXIS_X: {axis_x}, AXIS_Y: {axis_y}, SW: {sw_p}")
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed")
