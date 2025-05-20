#!/usr/bin/python3
import os
import threading
from playsound import playsound # type: ignore
import tkinter as tk
import csv
import os
from datetime import datetime

# Folder where CSV files will be saved
OUTPUT_FOLDER = os.path.expanduser('~/Desktop/barcode/scanner-data/')

def flash_success():
    '''
    Flash the screen to indicate a successful scan.
    '''
    original_color = "#f0f0f0"
    success_color = "#b5ffbb"

    frame.config(bg=success_color)
    root.config(bg=success_color)
    root.after(300, lambda: (frame.config(bg=original_color), root.config(bg=original_color)))

def flash_failure():
    '''
    Flash the screen to indicate a failed scan.
    '''
    original_color = "#f0f0f0"
    failure_color = "#e84646"

    frame.config(bg=failure_color)
    root.config(bg=failure_color)
    root.after(300, lambda: (frame.config(bg=original_color), root.config(bg=original_color)))

def play_error():
    '''
    Play an error sound.
    '''
    error_sound = os.path.expanduser('~/Desktop/barcode/error.mp3')
    playsound(error_sound)

def play_success():
    '''
    Play a success sound.
    '''
    success_sound = os.path.expanduser('~/Desktop/barcode/success.mp3')
    playsound(success_sound)

def on_enter(event):
    '''
    Handle the Enter key press event.
    
    Args:
        event: The event object containing information about the key press.

    This function retrieves the scanned data from the entry field, validates it,
    and writes it to a CSV file. It also plays a success or error sound and
    flashes the screen to indicate the result of the scan.
    If the input is not in the expected format, it displays an error message
    on the screen for 5 seconds.
    '''
    scan_data = entry.get().strip()
    entry.delete(0, tk.END)

    # Check if the scan_data is a valid student ID
    # Format: 909XXXXXXXXX (9 digits, starting with 909)
    # or a combination of student ID, date, and time
    if scan_data.isdigit() and len(scan_data) == 9 and scan_data.startswith("909"):
        student_id = scan_data
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
    else:
        parts = scan_data.split()
        if len(parts) == 3 and parts[0].isdigit() and len(parts[0]) == 9 and parts[0].startswith("909"):
            student_id, date_str, time_str = parts
            date_str = date_str.replace('/', '-')
            time_parts = time_str.split(":")
            time_str = ":".join(time_parts[:2])
        else:
            print("Unexpected input format:", scan_data)
            flash_failure()
            threading.Thread(target=play_error, daemon=True).start()

            # Display error message on the screen
            error_label = tk.Label(root, text="Check input and try again", font=("Helvetica", 24, "bold"), fg="black", bg="#f0f0f0")
            error_label.place(relx=0.5, rely=0.75, anchor="center")
            # Remove the error message after 5 seconds
            root.after(5000, error_label.destroy)
            return

    csv_filename = f"scans_{date_str}.csv"
    file_path = os.path.join(OUTPUT_FOLDER, csv_filename)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_id, date_str, time_str])

    flash_success()
    threading.Thread(target=play_success, daemon=True).start()

# Makes the program run in full screen
root = tk.Tk()
root.title("Barcode Scanner Logger")
root.attributes("-fullscreen", True)
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.place(relx=0.5, rely=0.5, anchor="center")

label = tk.Label(frame, text="Scan Student ID:", font=("Helvetica", 48, "bold"), bg="#f0f0f0")
label.pack(pady=20)

# Creates a text entry field for the barcode scanner
# The barcode scanner will act as a keyboard and type the scanned number into the entry field
entry = tk.Entry(frame, font=("Helvetica", 36), justify="center", width=30)
entry.pack(pady=10, ipadx=10, ipady=20)
entry.focus_set()

info_label = tk.Label(frame, text="You can either scan your ID card or manually type your 909 number and press Enter.", font=("Helvetica", 20), bg="#f0f0f0")
info_label.pack(pady=20)

exit_label = tk.Label(root, text="Press Escape to Exit", font=("Helvetica", 12), fg="gray", bg="#f0f0f0")
exit_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

# Bind the Enter key to the on_enter function
# and the Escape key to exit the program
entry.bind("<Return>", on_enter)
root.bind("<Escape>", lambda event: root.destroy())

root.mainloop()
