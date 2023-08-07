
# Code that estimates inertia with the csv file created from inertia.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import math


def estimate_inertia(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Extract the data from the DataFrame
    # position = df['position']
    commanded_torque = df['commanded torque']
    torque = df['torque']
    position = df['position']
    velocity = df['velocity']*(2*math.pi)
    window_size = 15
    smoothed_velocity_data = np.convolve(velocity, np.ones(window_size)/window_size, mode='valid')


    # This time interval is the interval between for loop in inertia.py. It is used to calculate gradient. 
    time_interval = 0.00467  # You can adjust this if you know the actual time interval
    angular_acceleration = np.gradient(smoothed_velocity_data, time_interval)
    # angular_acceleration = angular_acceleration*0.0003


    
    plt.plot(position)
    plt.plot(velocity)
    # plt.plot(angular_acceleration)
    # plt.plot(smoothed_velocity_data)
    # plt.plot(torque)
    # plt.plot(commanded_torque)
    plt.xlabel('Time (s)')
    plt.ylabel('Values')
    plt.title('Result: High tension')

    plt.ylim(-170, 170)
    plt.legend(["position", "velocity"], loc="upper left")
    plt.grid(True)
    plt.show()

    # Perform linear regression to estimate inertia
    torque_reshaped = np.array(commanded_torque[len(commanded_torque) - len(angular_acceleration):]).reshape(-1, 1)
    angular_acceleration_reshaped = np.array(angular_acceleration).reshape(-1, 1)

    # Fit linear regression model
    model = LinearRegression()
    model.fit(angular_acceleration_reshaped, torque_reshaped)

    # Get inertia from the slope of the linear regression
    inertia = model.coef_[0][0]

    # Plot the data points and the fitted line
    plt.scatter(angular_acceleration, commanded_torque[len(commanded_torque) - len(angular_acceleration):], label='Accel : Torque')
    plt.plot(angular_acceleration, model.predict(angular_acceleration_reshaped), color='red', label='Linear Regression')
    plt.xlabel('Angular Acceleration (rad/s^2)')
    plt.ylabel('Commanded Torque (N-m)')
    plt.title('Linear Regression for Inertia Estimation')
    plt.legend()
    plt.grid(True)
    plt.show()

    return inertia

if __name__ == "__main__":
    # csv_file_path = 'my_inertia/csv/data_log_interval.csv'  # Adjust the path accordingly
    csv_file_path = 'inertia/csv/data_log_interval.csv'
    estimated_inertia = estimate_inertia(csv_file_path)
    print(f"Estimated Inertia: {estimated_inertia} kg-m^2")
