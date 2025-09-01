import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# Dictionary to create our original and sketch Images
images = {"original": None,"sketch":None}

# Function to handle opening an image filw
def open_file():
    filepath = filedialog.askopenfilename()
    if not filepath: # If user dosen't select anything 
        
        return # nothing or do non
    img = cv2.imread(filepath) # Using opencv and store it in the img variable
    display_image(img, original=True) # Calling the display image function to show the original image to indicate the original image
    sketch_img = convert_to_sketch(img) # Calling the convert to sketch function to transform the image to a sketch
    display_image(sketch_img, original=False) # To display the sketch image passing false to indicate tht it is not the original

#Defining our convert to sketch function which will convert the image into a sketch-like version
def convert_to_sketch(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # First converting our image to grayscale
    inverted_img = cv2.bitwise_not(gray_img) # Invert the grayscale image to get its negative
    blurred_img = cv2.GaussianBlur(inverted_img,(21,21),sigmaX=0,sigmaY=0)  # Apply Gaussian blur to inverted image to smooth it out
    inverted_blur_img = cv2.bitwise_not(blurred_img) # Inverting the blurred image
    sketch_img = cv2.divide(gray_img, inverted_blur_img, scale=256.0) # Divide the gray image and the inverted blur image to get a sketch effect
    return sketch_img # return the resulting sketch image

# Defining our display image function that will handle showing images in our gui
def display_image(img, original):
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) if original else img # If it's the original image, we convert it to RGB colorspace otherwise leave it as is
    img_pil = Image.fromarray(img_rgb) # Converting our numpy array image to a pil image object
    img_tk = ImageTk.PhotoImage(image=img_pil) # Create a tkinter compatible photo image from the pil image
    
    # Store the image in the dictionary
    if original:
        images["original"] = img_pil # If we're dealing with a original image we store it inside the dictionary under the original key
    else:
        images["sketch"] = img_pil
    label = original_image_label if original else sketch_image_label # We choose which label to update whether it's the original or sketch image
    label.config(image=img_tk) # We update the selected image lable with the new tkinter photo image
    label.image = img_tk # Having a reference to the image to prevent it from being garbage collected

# Defining our save sketch funtion that will handle saving our sketch image
def save_sketch():
    if images["sketch"] is None: # if there's a sketch image to save, we save it, else  show error message
        messagebox.showerror("Error", "No sketch to save.")
        return
    sketch_filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files","*.png")]) #File dialog to let the user choose where to save their sketch it will also default to png files
    
     # if user actually selected a filepath
    if not sketch_filepath: # if they did not select filepath we stop here
        return
    # Save the PIL Image (sketch) to the file
    images["sketch"].save(sketch_filepath,"PNG")
    messagebox.showinfo("Saved", f"Sketch saved to {format(sketch_filepath)}.") # Letting the user know that their file has been saved

app = tk.Tk() # main window for the application using tkinter
app.title("Pencil Sketch Converter") # The title of our window
frame = tk.Frame(app) # creating the frame for our application
frame.pack(pady=10,padx=10) # Padding for our window for good look
original_image_label = tk.label(frame) # Creating a label to display the original image
original_image_label.grid(row=0, column=5, pady=5) # Positionig the original image label in the frame with some padding
sketch_image_label = tk.label(frame) # Creating another label to name and display the sketch image
sketch_image_label.grid(row=0,column=1, padx=5, pady=5) # Positioning the sketch image label next to the original image label
btn_frame = tk.Frame(app) # Frame to hold our buttons
btn_frame.pack(pady=10) # Another button frame below our first button frame 
open_button = tk.Button(btn_frame,text="Open Image", command=open_file) # Another button called open file which call the "Open File" function when clicked
open_button.grid(row=0,column=0,padx=5) # Positioning the open image button in the button frame
save_button = tk.Button(btn_frame,text="save sketch",command=save_sketch) # Button called "Save Sketch" that will call the "save_sketch" function when clicked
save_button.grid(row=0,column=1,padx=5) # Positioning the save sketch button next to the open image button

app.mainloop() # We start our application using thr main event loop, which will our app window responsive to user actions



        
           
    
    
       
    
