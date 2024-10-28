import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def center_window(window, width=400, height=300):
    # Center the window on the screen with fixed size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)  # Disable resizing

def truncate_path(path, max_length=30):
    if len(path) <= max_length:
        return path
    head, tail = os.path.split(path)
    truncated = f"{head[:max_length//2 - 3]}...{tail[-(max_length//2):]}"
    return truncated

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        global img
        img = Image.open(file_path)
        img_label.config(text="Loaded image:")
        truncated_path = truncate_path(file_path, max_length=40)
        path_label.config(text=truncated_path)  # Display truncated path
        original_size_label.config(text=f"Original Size: {img.size[0]} x {img.size[1]}")
        width_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
        width_entry.insert(0, img.size[0])
        height_entry.insert(0, img.size[1])
    else:
        img_label.config(text="No image loaded")

def resize_and_save():
    try:
        if resize_var.get():
            width = int(width_entry.get())
            height = int(height_entry.get())
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
        else:
            resized_img = img

        quality = int(quality_entry.get())
        optimize = optimize_var.get()
        
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if save_path:
            resized_img.save(save_path, quality=quality, optimize=optimize)
            messagebox.showinfo("Success", f"Image saved to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Image Resizer")
center_window(root, width=300, height=300)

# Fixed form layout with adjusted label widths
tk.Button(root, text="Load Image", command=load_image).grid(row=0, column=0, padx=5, pady=5)
img_label = tk.Label(root, text="No image loaded", width=30, anchor="w")
img_label.grid(row=0, column=1, padx=5, pady=5)

path_label = tk.Label(root, text="", width=30, anchor="w")  # Display truncated path in single line
path_label.grid(row=1, column=1, padx=5, pady=5)

original_size_label = tk.Label(root, text="Original Size: N/A", width=30, anchor="w")
original_size_label.grid(row=2, column=1, padx=5, pady=5)

resize_var = tk.BooleanVar()
resize_check = tk.Checkbutton(root, text="Enable Resize", variable=resize_var)
resize_check.grid(row=3, column=0, padx=5, pady=5)

tk.Label(root, text="Width:").grid(row=4, column=0, padx=5, pady=5)
width_entry = tk.Entry(root)
width_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Height:").grid(row=5, column=0, padx=5, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Quality:").grid(row=6, column=0, padx=5, pady=5)
quality_entry = tk.Entry(root)
quality_entry.insert(0, "70")
quality_entry.grid(row=6, column=1, padx=5, pady=5)

optimize_var = tk.BooleanVar()
optimize_check = tk.Checkbutton(root, text="Optimize", variable=optimize_var)
optimize_check.grid(row=7, column=1, padx=5, pady=5)

tk.Button(root, text="Resize and Save", command=resize_and_save).grid(row=8, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
