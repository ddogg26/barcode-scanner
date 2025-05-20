# barcode-scanner
Simple python GUI application for logging Columbus State University student ID scans to CSV files. Designed for use with barcode scanners that emulate keyboard input.

### Features
* Easy to use interface
* Logs scans to daily CSV files
* Plays success/error sounds and flashes the screen for user feedback
* Accepts both scanned and manually entered IDs

### Requirements
* Python 3.x
* tkinter    (```sudo apt install python3-tk```)
* playsound  (```pip install playsound```)

### Usage
1. Place ```barcode.py``` in a folder (```~/Desktop/barcode/```)
2. Place ```error.mp3``` and ```success.mp3``` files in the same folder
3. Run the program (```python3 barcode.py```)
4. Scan a student ID or type it in manually and press enter
5. Press Escape to exit

### Output
* Scan data is saved as CSV files in ```~/Desktop/barcode/scanner-data/```, one file per day

### Notes
* Student IDs must be 9 digits starting with ```909```
* The barcode scanner must be setup to end with a line feed (```\n```) in order to emulate pressing Enter
