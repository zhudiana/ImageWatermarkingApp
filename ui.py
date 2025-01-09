import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from watermark import add_watermark
from utils import select_file

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.configure(bg="#202020")
        self.root.geometry("800x600")

        # Main container to center elements
        self.main_frame = tk.Frame(root, bg="#202020")
        self.main_frame.pack(expand=True)

        # Load and Display Logo
        self.load_logo()

        # Title Label
        self.title_label = tk.Label(
            self.main_frame, text="Add Watermark", font=("Arial", 28, "bold"),
            fg="white", bg="#202020"
        )
        self.title_label.pack(pady=20)

        # Select File Button
        self.select_button = tk.Button(
            self.main_frame, text="Select Files", command=self.select_file,
            font=("Arial", 14), bg="#4A90E2", fg="white", relief="flat",
            padx=20, pady=10
        )
        self.select_button.pack(pady=10)


        # Footer Message
        self.footer_label = tk.Label(
            root, text="Files stay private. We process files on your device. No data is sent to servers.",
            font=("Arial", 10), fg="gray", bg="#202020"
        )
        self.footer_label.pack(side="bottom", pady=10)

    def load_logo(self):
        """Load and display the logo"""
        try:
            logo_image = Image.open("images/logo.png").convert("RGBA")
            resized_logo = logo_image.resize((150, 150))
            self.logo_photo = ImageTk.PhotoImage(resized_logo)
            self.logo_label = tk.Label(self.main_frame, image=self.logo_photo, bg="#202020")
            self.logo_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo not found! Please check the images folder.")

    def select_file(self):
        """Open file dialog and handle images selection"""
        file_path = select_file()
        if file_path:
            messagebox.showinfo("File Selected", f"File selected: {file_path}")
        # else:
        #     messagebox.showwarning("No File Selected", "Please select a file.")

    def open_watermark_window(self):
        # Open a new window and display the selected images
        new_window = tk.Toplevel(self.root)
        new_window.title("Add Watermark")
        img = Image.open(self.image_path)
        img.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(new_window, image=photo)
        label.image = photo  # Prevent garbage collection
        label.pack()

        # Add Watermark Button
        watermark_button = tk.Button(new_window, text="Add Watermark", command=lambda: add_watermark(self.image_path, new_window), font=("Arial", 12))
        watermark_button.pack(pady=10)
