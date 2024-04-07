import tkinter as tk
import customtkinter
from tkinter import ttk, filedialog
import os
import pyautogui as py
import subprocess
import ctypes, sys
import findInteractables as fi

# Requires Admin permission (CMD) because findInteractables.py needs Admin permission
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        selected_option = dropdown_interactable.get()
        if selected_option and selected_option != "- Select -":
            file_name = selected_option.lower().replace(" ", "_") + ".png"  # Generate the filename based on the selected option
            file_destination = os.path.join(current_dir, "images", file_name)  # Set the destination path for the new image
            os.replace(file_path, file_destination)  # Replace the old image with the uploaded image
            replaced_label.configure(text="Image replaced: " + file_name)  # Update the label with the replaced image filename

# The current working directory is the directory where the script is running from
current_dir = os.getcwd()

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Cats & Soup Interactables Clicker")

# Adding UI Elements
# Upload Interactable Image label
upload_title = customtkinter.CTkLabel(app, text="Upload Interactable Image")
upload_title.place(x = 30, y = 30, anchor="nw")

# Update Coordinate label
update_title = customtkinter.CTkLabel(app, text="Update Coordinate")
update_title.place(x = 30, y = 140, anchor="nw")

# Dropdown menu options
options = [
    "Slug",
    "Frog",
    "Gift",
    "Jar Fairy",
    "Butterfly"
]

# Dropdown menu: Upload Interactable Image
dropdown_interactable = customtkinter.CTkComboBox(app, values=options, state="readonly")
dropdown_interactable.set("- Select -")  # Set default value to "- Select -"
dropdown_interactable.place(x = 30, y = 60, anchor="nw")

# Dropdown menu: Update Coordinates
dropdown_coordinate = customtkinter.CTkComboBox(app, values=options, state="readonly")
dropdown_coordinate.set("- Select -")  # Set default value to "- Select -"
dropdown_coordinate.place(x = 30, y = 170, anchor="nw")

# Upload button
upload_button = customtkinter.CTkButton(app, text="Upload Image", command=open_file)
upload_button.place(x = 230, y = 60, anchor="nw")

# Label to display replaced image filename
replaced_label = customtkinter.CTkLabel(app, text="", font=("Arial", 10))
replaced_label.place(x = 240, y = 90, anchor="nw")

# Function to update the text field with mouse coordinates
def update_text_field():
    # Get mouse position using pyautogui
    mouse_position = py.position()
    
    # Update text field variable with mouse coordinates
    coordinates_var.set(f"x: {mouse_position.x}, y: {mouse_position.y}")
    
    # Schedule the next update after 100 milliseconds
    app.after(100, update_text_field)

# Create a Tkinter variable for the text bar field
coordinates_var = tk.StringVar()
coordinates_var.set("")  # Initialize with an empty string

# Create the text bar field
text_bar = ttk.Entry(app, width=40, state="readonly", textvariable=coordinates_var)  # Set the state to "readonly"
text_bar.place(x = 231, y = 210)

# Create the button to start tracking
track_button = customtkinter.CTkButton(app, text="Track", command=update_text_field)
track_button.place(x = 230, y = 170)


# Change the working directory to the directory containing both scripts
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Function to run findInteractables.py
def start_find_interactable():
    try:
        if is_admin():
            print("Executing subprocess...")
            # Run the findInteractables.py script
            os.system('start cmd /k "python findInteractables.py"')
            output="hello"
            print("Subprocess executed successfully.")
        else:
            output = "Error: Script requires administrator privileges."
    # except subprocess.CalledProcessError as e:
    #     # Handle errors if the script fails to execute
    #     output = f"Error: {e.returncode}, {e.output}"
    #     print(f"Subprocess error: {e}")
    except Exception as e:
        # Handle other exceptions
        output = f"Error: {str(e)}"
        print(f"Exception: {e}")
    
    # Update the text in the text box
    output_box.delete("1.0", "end")  # Clear previous text
    output_box.insert("1.0", output)


# Create a button to start findInteractables.py
start_button = customtkinter.CTkButton(app, text="Start", command=start_find_interactable)
start_button.place(x = 100, y = 400)

# Create a text box to display the output of findInteractables.py
output_box = tk.Text(app, width = 30, height = 10, bg="white", state=tk.DISABLED)
output_box.place(x = 550, y = 380)


# Run app
app.mainloop()