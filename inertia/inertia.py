#!/usr/bin/python3 -B

# Code that gives sinusoidal torque, and gets position, velocity data

import asyncio
import csv
import math
import moteus
import time
import numpy as np
import matplotlib.pyplot as plt

torque = [0]
position = [0]
velocity = [0]
commanded_torque = [0]

time_intervals = [] # List to store time intervals
prev_time = time.time() # Record the starting time

filenames = ['torque', 'position', 'velocity','commanded torque','time interval']
csvfile = open('inertia/csv/0803.csv', 'w', newline='')
data_writer = csv.writer(csvfile)
data_writer.writerow(filenames)


async def main():

    global prev_time
    # By default, Controller connects to id 1, and picks an arbitrary
    # CAN-FD transport, prefering an attached fdcanusb if available.
    qr = moteus.QueryResolution()
    qr._extra = {
        moteus.Register.CONTROL_TORQUE: moteus.F32,
        moteus.Register.COMMAND_Q_CURRENT: moteus.F32,
        moteus.Register.Q_CURRENT: moteus.F32,
    }
    c = moteus.Controller(query_resolution=qr)

    for x in range(2000):

        # We should calculate time interval in order to differentiate velocity
        current_time = time.time()
        time_interval = current_time - prev_time # Calculate the time interval
        time_intervals.append(time_interval)
        prev_time = current_time


        # free: 0.02
        # timing belt: 0.1~0.2 (max 0.35)
        fftorque = 0.35 * math.sin(math.pi*x/200)
        # response = (await c.set_current(d_A = 0, q_A = cur, query=True))
        response = (await c.set_position(position=math.nan, velocity = 0,kp_scale=0, kd_scale=0,
                                         feedforward_torque=fftorque,query=True))
        # response = (await c.set_torque_made(command_torque = tor, query=True))
    

        commanded_torque.append(fftorque)
        torque.append(response.values[moteus.Register.TORQUE])
        position.append(response.values[moteus.Register.POSITION])
        velocity.append(response.values[moteus.Register.VELOCITY])

        data_writer.writerow([torque[-1], position[-1], velocity[-1],fftorque,time_interval])

        await asyncio.sleep(0.001)  
        
    response = (await c.set_stop(query = True))

    
    plt.plot(commanded_torque)
    plt.plot(torque)
    plt.plot(position)
    plt.plot(velocity)
    plt.plot(time_intervals)
    plt.legend(["commanded torque","torque","position","velocity", "interval"])

    plt.show()


asyncio.run(main())






