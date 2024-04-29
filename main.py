import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from tkinter import ttk

# UI
root = tk.Tk()
root.geometry("1000x600")
root.title("Photo Editor")
root.config(bg="white")

# Global variables
pen_color = "black"
pen_size = 5
file_path = ""
untouched = ""
brightness_value = 1.0
rotation_angle = 0

# ALLOWS USERS TO EDIT AN IMAGE OF THEIR CHOICE
def add_image():
    global file_path, rotation_angle, untouched
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image") 
    untouched = file_path
    if file_path:
        rotation_angle = 0  # Reset rotation angle
        display_image()
        rotate_button.config(state="normal")
        flip_button.config(state="normal")

def display_image():
    global file_path, rotation_angle
    image = Image.open(file_path)
    # Rotate image based on rotation angle
    rotated_image = image.rotate(rotation_angle, expand=True)
    width, height = int(rotated_image.width / 2), int(rotated_image.height / 2)
    rotated_image = rotated_image.resize((width, height), Image.BILINEAR)
    image = ImageTk.PhotoImage(rotated_image)
    canvas.config(width=image.width(), height=image.height())
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")
    toggle_filter_combobox("normal")
    save_button.config(state="normal")
    brightness_slider.config(state="normal")

# Change the brightness of the image
def change_brightness(value):
    global brightness_value
    brightness_value = float(value)
    apply_filter("Brightness")

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def change_size(size):
    global pen_size
    pen_size = size

# ENABLES PEN DRAWING
def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

def clear_canvas():
    canvas.delete("all")
    toggle_filter_combobox("disabled")
    save_button.config(state="disabled")
    brightness_slider.config(state="disabled")
    rotate_button.config(state="disabled")
    flip_button.config(state="disabled")

def revert():
    global untouched
    rotation_angle = 0
    image = Image.open(untouched)
    # Rotate image based on rotation angle
    rotated_image = image.rotate(rotation_angle, expand=True)
    width, height = int(rotated_image.width / 2), int(rotated_image.height / 2)
    rotated_image = rotated_image.resize((width, height), Image.BILINEAR)
    image = ImageTk.PhotoImage(rotated_image)
    canvas.config(width=image.width(), height=image.height())
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")
    toggle_filter_combobox("normal")
    save_button.config(state="normal")
    brightness_slider.config(state="normal")
# FILTER PRESETS
def apply_filter(filter):
    if not file_path:
        return
    image = Image.open(file_path)
    rotated_image = image.rotate(rotation_angle, expand=True)
    width, height = int(rotated_image.width / 2), int(rotated_image.height / 2)
    rotated_image = rotated_image.resize((width, height), Image.BILINEAR)
    if filter == "Black and White":
        rotated_image = ImageOps.grayscale(rotated_image)
    elif filter == "Blur":
        rotated_image = rotated_image.filter(ImageFilter.BLUR)
    elif filter == "Sharpen":
        rotated_image = rotated_image.filter(ImageFilter.SHARPEN)
    elif filter == "Smooth":
        rotated_image = rotated_image.filter(ImageFilter.SMOOTH)
    elif filter == "Emboss":
        rotated_image = rotated_image.filter(ImageFilter.EMBOSS)
    elif filter == "Brightness":
        rotated_image = ImageEnhance.Brightness(rotated_image).enhance(brightness_value)

    image = ImageTk.PhotoImage(rotated_image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# allow the filter combobox to appear ONLY when an image is selected
def toggle_filter_combobox(state):
    filter_combobox.config(state=state)

# ability to save edited image
def save_image():
    if not file_path:
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        canvas.postscript(file=save_path + '.eps')
        img = Image.open(save_path + '.eps')
        img.save(save_path)

# Rotate the image clockwise by 90 degrees
def rotate_image():
    global rotation_angle
    rotation_angle = (rotation_angle - 90) % 360
    display_image()

# Flip the image horizontally (mirror the image)
def flip_image():
    global file_path
    if file_path:
        image = Image.open(file_path)
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        flipped_image.save(file_path)
        display_image()

# creates left frame
left_frame = tk.Frame(root, width=200, height=600, bg="white")
left_frame.pack(side="left", fill="y")

# canvas size
canvas = tk.Canvas(root, width=750, height=600)
canvas.pack()

# Image Button
image_button = tk.Button(left_frame, text="Upload Image", command=add_image, bg="white")
image_button.pack(pady=15)

# Color Button
color_button = tk.Button(
    left_frame, text="Change Pen Color", command=change_color, bg="white")
color_button.pack(pady=5)

# Pen Size
pen_size_frame = tk.Frame(left_frame, bg="white")
pen_size_frame.pack(pady=5)

# PEN SIZE RADIO BUTTONS:
# small pen
pen_small = tk.Radiobutton(
    pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg="white")
pen_small.pack(side="left")

# medium pen
pen_medium = tk.Radiobutton(
    pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg="white")
pen_medium.pack(side="left")
pen_medium.select()

# large pen
pen_large = tk.Radiobutton(
    pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg="white")
pen_large.pack(side="left")

# Filter Combobox
filter_label = tk.Label(left_frame, text="Select Filter", bg="white")
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=["Black and White", "Blur", "Emboss", "Sharpen", "Smooth"], state="disabled")
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>",
                     lambda event: apply_filter(filter_combobox.get()))

# Brightness Slider
brightness_label = tk.Label(left_frame, text="Brightness", bg="white")
brightness_label.pack()
brightness_slider = tk.Scale(left_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=change_brightness, state="disabled")
brightness_slider.pack()

# Rotate and Flip Buttons
rotate_flip_frame = tk.Frame(left_frame, bg="white")
rotate_flip_frame.pack(pady=5)

# Rotate Button
rotate_button = tk.Button(
    rotate_flip_frame, text="Rotate", command=rotate_image, bg="white", state="disabled")
rotate_button.pack(side="left", padx=5)

# Flip Button
flip_button = tk.Button(
    rotate_flip_frame, text="Flip", command=flip_image, bg="white", state="disabled")
flip_button.pack(side="left", padx=5)

# Save Button
save_button = tk.Button(left_frame, text="Save As", command=save_image, bg="white", state="disabled")
save_button.pack(pady=10)

# Clear Button
clear_button = tk.Button(left_frame, text="Clear All",
                         command=clear_canvas, bg="#FF9797")
clear_button.pack(pady=10)

# Draw motion
canvas.bind("<B1-Motion>", draw)

root.mainloop()
