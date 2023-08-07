#!/usr/bin/python3 -B

# This is code that can calibrate motor using loadcell, arudino.

import asyncio
import serial
import csv
import math
import moteus
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Make sure that torque_constant is set properly.
# It is calculated as "torque_constant = 0.78 * 60 / (2 * pi * kv)", so you should change kv when you change motor
kv = 267.168
torque_constant = 60*0.78/(kv*2*math.pi) 
torque = [0]
commanded_Q_current = [0]
current = [0]
write_csv = True

def extract_numeric_value(line):
    parts = line.split()
    for part in parts:
        try:
            value = float(part)
            return value
        except ValueError:
            pass
    return None

def linear(curG,torque):
        
    # Convert curG and torque to NumPy arrays
    curG = np.array(curG)
    torque = np.array(torque)

    # Create a linear regression model
    regression_model = LinearRegression()

    # Reshape the data to match the expected input shape for the model
    curG_reshaped = curG.reshape(-1, 1)

    # Fit the model to the data
    regression_model.fit(curG_reshaped, torque)

    # Predict torque based on curG
    predicted_torque = torque_constant * curG

    # Plot the scatter points
    plt.scatter(curG, torque, label='After')

    # Plot the linear regression line
    plt.plot(curG, predicted_torque, color='red', label='Before')

    # Set the axis labels
    plt.xlabel('Iq')
    plt.ylabel('torque')

    # Set the title
    plt.title('Current-Torque')

    # Set the legend
    plt.legend()

    # Show the plot
    plt.show()

# Function to handle serial communication and save data to CSV
async def read_serial_and_save_data(ser, commanded_Q_current_data,torque_real):
    with open('calib_with_loadcell/calib_mj5208_csv/data_log.csv', 'w', newline='') as csvfile:

        filenames = ['Commanded I', 'Weight','torque_real']

        # Create a CSV writer object with the header row
        data_writer = csv.writer(csvfile)

        data_writer.writerow(filenames) 

        while write_csv:
            if ser.in_waiting > 0:
                line = ser.readline().decode().strip()
                print("Received data:", line)
                numeric_value = extract_numeric_value(line)
                if commanded_Q_current_data[-1] != 0 and numeric_value>1.0:
                    # Save the timestamp and the data to the CSV file
                    data_writer.writerow([commanded_Q_current_data[-1], numeric_value,torque_real[-1]])

            await asyncio.sleep(0.001)


async def main():

    await asyncio.sleep(10)
    # By default, Controller connects to id 1, and picks an arbitrary
    # CAN-FD transport, prefering an attached fdcanusb if available.
    qr = moteus.QueryResolution()
    qr._extra = {
        moteus.Register.CONTROL_TORQUE: moteus.F32,
        moteus.Register.COMMAND_Q_CURRENT: moteus.F32,
        moteus.Register.TORQUE_ERROR: moteus.F32,
        moteus.Register.Q_CURRENT: moteus.F32,
    }
    c = moteus.Controller(query_resolution=qr)


    # In the for loop, current goes up until value you set.
    # Be aware that your current should not go over 50A.
    for x in range(4000):
        cur = -x/80.0 # Be aware of your maximum current and sign!!
        response = (await c.set_current(d_A = 0, q_A = cur, query=True))

        # response = (await c.set_position())
        # response = (await c.set_torque_made(command_torque = tor, query=True))
    
        # commanded_torque[x] = -cur
        torque.append(-response.values[moteus.Register.TORQUE])
        commanded_Q_current.append(-response.values[moteus.Register.COMMAND_Q_CURRENT])
        current.append(-response.values[moteus.Register.Q_CURRENT])

        await asyncio.sleep(0.001)  
        
    response = (await c.set_stop(query = True))

    global write_csv
    write_csv = False
    
    linear(commanded_Q_current,torque)

    plt.plot(torque)
    # plt.plot(commanded_torque)
    plt.plot(current)
    plt.plot(commanded_Q_current)

    plt.legend(["torque","Iq","commanded_Iq"])

    plt.show()

# Create a serial connection of arduino
# You should change it to your existing port
ser = serial.Serial('/dev/cu.usbmodem11301', 57600)

# Run both tasks concurrently using asyncio.gather()
async def run_tasks():
    await asyncio.gather(main(), read_serial_and_save_data(ser, commanded_Q_current,torque))

# Run the event loop
asyncio.run(run_tasks())







