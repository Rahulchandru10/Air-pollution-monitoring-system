import tkinter as tk
from collections import deque

import matplotlib.pyplot as plt
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Connect to the Arduino via serial
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the appropriate port name

# Function to get air quality level
def get_air_quality_level(ppm):
    if ppm <= 1000:
        return "Good", "green"
    elif ppm <= 2000:
        return "Not Good", "yellow"
    elif ppm <= 5000:
        return "Dangerous", "blue"
    elif ppm <= 40000:
        return "More Dangerous", "darkviolet"
    else:
        return "Hazardous", "red"

# Function to read ppm values and update GUI
def read_serial():
    try:
        ppm_value = ser.readline().decode().strip()  # Read the ppm value from Arduino
        ppm = float(ppm_value)
        air_quality, color = get_air_quality_level(ppm)

        ppm_label.config(text=f"Air Quality (PPM): {ppm:.2f} ppm")
        air_quality_label.config(text=f"Air Quality: {air_quality}")
        color_box.config(bg=color)

        ppm_values.append(ppm)
        time_values.append(len(ppm_values))

        line.set_data(time_values, ppm_values)
        ax.relim()
        ax.autoscale_view()

        canvas.draw()

        ppm_label.after(1000, read_serial)  # Read again after 1 second
    except:
        ppm_label.config(text="Error reading air quality")

# Create the GUI window
root = tk.Tk()
root.title("Air Quality Monitoring System")

# Create a title label
title_label = tk.Label(root, text="Air Quality Monitoring System", font=("Times New Roman", 20))
title_label.grid(row=0, columnspan=4, pady=20)  # Use grid instead of pack

# Create a label to display ppm value
ppm_label = tk.Label(root, text="Air Quality (PPM): -", font=("Times New Roman", 16))
ppm_label.grid(row=1, columnspan=4)  # Use grid instead of pack

# Create a label to display air quality level with colored box
air_quality_frame = tk.Frame(root)
air_quality_frame.grid(row=2, columnspan=4)  # Use grid instead of pack

color_box = tk.Label(air_quality_frame, text="", width=2, height=1)
color_box.grid(row=0, column=0, padx=10)  # Use grid instead of pack

air_quality_label = tk.Label(air_quality_frame, text="Air Quality: -", font=("Times New Roman", 16))
air_quality_label.grid(row=0, column=1)  # Use grid instead of pack

# Table headers
headers = ["PPM Range", "Condition", "Indication"]

for col, header in enumerate(headers):
    header_label = tk.Label(root, text=header, font=("Times New Roman", 14, "bold"))
    header_label.grid(row=3, column=col, padx=10, pady=5)

# Table data
data = [
    ("350-1,000 ppm", "Good", "green"),
    ("1,000-2,000 ppm", "Not Good", "yellow"),
    ("2,000-5,000 ppm", "Dangerous", "blue"),
    ("5,000-40,000 ppm", "More Dangerous", "darkviolet"),
    (">40,000 ppm", "Hazardous", "red")
]

for row, (ppm_range, condition, color) in enumerate(data, start=4):
    ppm_range_label = tk.Label(root, text=ppm_range, font=("Times New Roman", 12))
    ppm_range_label.grid(row=row, column=0, padx=10, pady=5)

    condition_label = tk.Label(root, text=condition, font=("Times New Roman", 12))
    condition_label.grid(row=row, column=1, padx=10, pady=5)

    colored_box = tk.Label(root, text="", bg=color, width=10, height=1)
    colored_box.grid(row=row, column=2, padx=10, pady=5)

# Create a figure and subplot for the real-time graph
fig = plt.figure(figsize=(6, 3), dpi=80)
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('PPM Value')

# Create an initial empty deque to store ppm values for the graph
ppm_values = deque(maxlen=500)
time_values = deque(maxlen=500)

# Create a line object for the graph
line, = ax.plot([], [], 'r-')

# Create a canvas to embed the matplotlib figure into the tkinter GUI
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=9, column=0, columnspan=3, pady=10)  # Place the graph below the table

# Start reading ppm values and updating the GUI
read_serial()

# Run the GUI event loop
root.mainloop()
