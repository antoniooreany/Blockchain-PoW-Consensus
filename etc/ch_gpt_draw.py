#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a ch_gpt_draw and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import numpy as np
import matplotlib.pyplot as plt

# Sample mock data for Mining_time and Dual_difficulty
time_series = np.linspace(0, 100, 50)  # Time axis (x-axis)
Mining_time = np.random.uniform(0, 10, 50)  # Mining_time data (y-axis)
Dual_difficulty = np.random.uniform(1, 20, 50)  # Dual_difficulty data (secondary axis)
BASE = 0.8  # Circle diameter based on BASE parameter

# Creating the plot
fig, ax1 = plt.subplots()

# Plot Dual_difficulty with a regular line plot
ax1.plot(time_series, Dual_difficulty, label="Dual Difficulty", color='blue', linewidth=2)

# Create the secondary y-axis for Mining_time
ax2 = ax1.twinx()

# Plot circles for Mining_time with size based on BASE
ax2.scatter(time_series, Mining_time, s=(BASE * 100)**2, color='red', label='Mining Time', alpha=0.6)

# Adding labels, legend, and grid
ax1.set_xlabel('Time')
ax1.set_ylabel('Dual Difficulty', color='blue')
ax2.set_ylabel('Mining Time', color='red')

ax1.grid(True)

# Combine legends
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

plt.show()
