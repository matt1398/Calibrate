import serial
import asyncio
import moteus
import math

# Setting port for arduino joystick
port = '/dev/cu.usbmodem11301'
ser = serial.Serial(port, 9600, timeout=1)

# Read serial from your arduino joystick
async def read_serial():
    global axis_x, axis_y, sw_p
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            values = line.split(' ')
            if len(values) == 3:
                axis_x, axis_y, sw_p = map(int, values)
        print(f"AXIS_X: {axis_x}, AXIS_Y: {axis_y}, SW: {sw_p}")
        await asyncio.sleep(0.5)

servo_bus_map = {
  1:[1,2],
}
# main code that moves motor with given joystick movements
async def c1():
    qr = moteus.QueryResolution()
    c1 = moteus.Controller(id=1, query_resolution=qr) # Controller for motor 1
    while True:
        velocity_x = 0

        if sw_p == 0:  # Stop condition
            await c1.set_stop(query=True)
        else:
            if axis_x < 256:
                velocity_x = 0.2
            elif axis_x > 768:
                velocity_x = -0.2

            await c1.set_position(position=math.nan, velocity=velocity_x, maximum_torque=0.2)

        await asyncio.sleep(0.001)

async def c2():
    qr = moteus.QueryResolution()
    c2 = moteus.Controller(id=2, query_resolution=qr) # Controller for motor 2
    while True:
        velocity_y = 0
        if sw_p == 0:  # Stop condition
            await c2.set_stop(query=True)
        else:

            if axis_y < 256:
                velocity_y = 0.3
            elif axis_y > 768:
                velocity_y = -0.3

            await c2.set_position(position=math.nan, velocity=velocity_y, maximum_torque=0.2)

        await asyncio.sleep(0.001)

async def run_tasks():
    await asyncio.gather(c1(), c2(), read_serial())

axis_x, axis_y, sw_p = 512, 512, 1

try:
    asyncio.run(run_tasks())
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed")
