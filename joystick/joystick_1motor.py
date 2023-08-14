import serial
import asyncio
import moteus
import math

# Setting port for arduino joystick
port = '/dev/cu.usbmodem1301'
ser = serial.Serial(port, 9600, timeout=1)


# Read serial from your arduino joystick
async def read_serial():
    global axis_x, axis_y, sw_p  # These will be shared with main()
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            values = line.split(' ')
            if len(values) == 3:
                axis_x, axis_y, sw_p = map(int, values)  # Convert to integers
        print(f"AXIS_X: {axis_x}, AXIS_Y: {axis_y}, SW: {sw_p}")
        await asyncio.sleep(0.5)  # Match the Arduino's delay



# main code that moves motor with given joystick movements
async def main():
    qr = moteus.QueryResolution()
    c = moteus.Controller(query_resolution=qr)
    print(f"Controller ID: {c.id}") # Print the controller ID
    while True:

        velocity = 0  # Default velocity
        if sw_p == 0:  # Stop condition
            response = await c.set_stop(query=True) 
        elif axis_y < 256:
            velocity = 0.3
        elif axis_y > 768:
            velocity = -0.3

        if sw_p != 0:  # If not stopped, set the velocity
            response = await c.set_position(position=math.nan, velocity=velocity, maximum_torque=0.2)
        await asyncio.sleep(0.001)

async def run_tasks():
    await asyncio.gather(main(), read_serial())

axis_x, axis_y, sw_p = 512, 512, 1  # Global variables to store serial values

try:
    asyncio.run(run_tasks())
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed")