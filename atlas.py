import tkinter as tk
from main import main

def button_click():
    # Add your code here to handle button click event
    main()

# Create the main window
window = tk.Tk()

# Add widgets to the window
label = tk.Label(window, text="Hello, GUI!")
label.pack()

button = tk.Button(window, text="Click Me", command=button_click)
button.pack()

# Start the main event loop
window.mainloop()