import tkinter as tk
import subprocess

# function to run the Face detection Python code
def run_code1():
    subprocess.call(['python', 'facedetect.py'])

# function to run the Face upload with photo Python code
def run_code2():
    subprocess.call(['python', 'clickphoto.py'])

# function to run the Face upload with stored video Python code
def run_code3():
    subprocess.call(['python', 'video.py'])
# function to run the Face upload with live video Python code
def run_code4():
    subprocess.call(['python', 'video2.py'])
# create the GUI window
root = tk.Tk()

# create the first button
button1 = tk.Button(root, text="Detect Face", command=run_code1)
button1.pack()

# create the second button
button2 = tk.Button(root, text="Store Photos", command=run_code2)
button2.pack()

# create the third button
button3 = tk.Button(root, text="Stored Video face detection", command=run_code3)
button3.pack()

# create the third button
button4 = tk.Button(root, text="Live Video face detection", command=run_code4)
button4.pack()
# start the GUI loop
root.mainloop()
