
# This code optimizes the parameters for log function that Josh Pieper mentioned
# 1. You should set 'cutoff' looking at the graph, and change it.
# 2. After setting cutoff in this code, you can optimize the log graph
# 3. The parameters(cutoff_A, torque_scale, current_scale) should be set by tview
# Find details on https://jpieper.com/2020/07/31/dealing-with-stator-magnetic-saturation/ and
# https://github.com/mjbots/moteus/blob/main/docs/reference.md#servorotation_


import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import math
import numpy as np
from scipy.optimize import curve_fit




# Read the data from the CSV file
df = pd.read_csv('calib_with_loadcell/calib_mj5208_csv/data_log_50A_1.csv')

# Extract the 'Commanded I' and 'Weight' columns from the DataFrame
commanded_I = df['Commanded I']
weight = df['Weight']
torque_real = df['torque_real']

# This torque is calculated based on your setting of environments. We used stick which is 0.15m long.
# Since the weight should converted to torque, it uses this formula:
torque = weight*0.15*9.80665*0.001


# Make sure that torque_constant is set properly.
# It is calculated as "torque_constant = 0.78 * 60 / (2 * pi * kv)", so you should change kv when you change motor
kv = 267.168
torque_constant = 60*0.78/(kv*2*math.pi) 
predicted_torque = torque_constant * commanded_I


# you should set your cutoff looking through the graph
cutoff = 10
def log_function(commanded_I, torque_scale, current_scale):
    tc = torque_constant  # Assuming you have a constant value for 'tc'
    return cutoff * tc + torque_scale * np.log2(1 + (commanded_I - cutoff) * current_scale)

new_commanded_I = commanded_I[commanded_I > cutoff]
new_torque = torque[commanded_I > cutoff]



# Initial guesses for the parameters
initial_guess = [1.0,0.001]
# Perform the curve fitting
popt, _ = curve_fit(log_function, new_commanded_I, new_torque, p0=initial_guess)
torque_scale_fit, current_scale_fit = popt
fitted_torque = log_function(new_commanded_I, *popt)
print("Optimized torque scale:{}\nOptimized current scale:{}".format(torque_scale_fit,current_scale_fit))


# Plot the graph
plt.plot(commanded_I, predicted_torque, color='red', label='Torque-Current Before')

plt.scatter(commanded_I, torque, s = 5, label='Real Measured Torque')

plt.plot(new_commanded_I, fitted_torque, color='black', label='Optimized Log Model')

plt.plot(commanded_I, torque_real,color = 'orange', label = 'Torque-Current After')


plt.xlabel('I')
plt.ylabel('Torque')
plt.title('Relationship between I and torque')
plt.legend()
plt.show()

# mj5208:
# Optimized torque scale:1.384752074980803
# Optimized current scale:0.012323580702730978