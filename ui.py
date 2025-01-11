import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils import select_file

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.configure(bg="#202020")
        self.root.state('zoomed')

        # Main container for the home screen
        self.main_frame = tk.Frame(self.root, bg="#202020")
        self.main_frame.pack(expand=True)

        # Load and Display Logo (Resized for Proportional Look)
        self.load_logo()

        # Title Label
        self.title_label = tk.Label(
            self.main_frame, text="Add Watermark", font=("Arial", 28, "bold"),
            fg="white", bg="#202020"
        )
        self.title_label.pack(pady=(10,10))

        # Select File Button (Soft Blue for Home Window)
        self.select_button = tk.Button(
            self.main_frame, text="Select File", command=self.select_file,
            font=("Arial", 18), bg="#4A90E2", fg="white", relief="flat",
            padx=25, pady=12
        )
        self.select_button.pack(pady=(10, 50))

        # Footer Message
        self.footer_label = tk.Label(
            self.root, text="Files stay private. We process files on your device. No data is sent to servers.",
            font=("Arial", 12), fg="gray", bg="#202020"
        )
        self.footer_label.pack(side="bottom", pady=10)

    def load_logo(self):
        """Load and display the logo (Resized for Proportional Look)"""
        try:
            logo_image = Image.open("images/logo.png").convert("RGBA")
            resized_logo = logo_image.resize((200, 200))
            self.logo_photo = ImageTk.PhotoImage(resized_logo)
            self.logo_label = tk.Label(self.main_frame, image=self.logo_photo, bg="#202020")
            self.logo_label.pack(pady=(50, 10))
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo not found! Please check the images folder.")

    def select_file(self):
        """Open a file dialog for selecting **a single image only**"""
        file_path = select_file()
        if file_path:
            self.open_new_window([file_path])  # Single file passed as a list
    def open_new_window(self, file_paths):
        """Replaces the current window with the image display window"""
        self.main_frame.pack_forget()
        self.footer_label.pack_forget()

        # NEW WINDOW LAYOUT: BUTTONS IN THE SAME ROW (TOP BAR)
        self.top_bar = tk.Frame(self.root, bg="#303030", height=60)
        self.top_bar.pack(fill="x")

        # Home Button (Now Returns to the Previous Window)
        self.home_button = tk.Button(
            self.top_bar, text="Home", command=self.go_home,
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat"
        )
        self.home_button.pack(side="left", padx=10, pady=10)

        # Add Files Button (Select One Image Only)
        self.add_files_button = tk.Button(
            self.top_bar, text="Add File", command=self.add_single_file,
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat"
        )
        self.add_files_button.pack(side="left", padx=10, pady=10)

        # Clear Button (Disabled Initially)
        self.clear_button = tk.Button(
            self.top_bar, text="Clear", command=self.clear_images,
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat", state="disabled"
        )
        self.clear_button.pack(side="left", padx=10, pady=10)

        # Next Step Button (Soft Blue)
        self.next_step_button = tk.Button(
            self.top_bar, text="Next Step ➡️", command=self.next_step,
            font=("Arial", 12), bg="#4A90E2", fg="white", relief="flat"
        )
        self.next_step_button.pack(side="right", padx=10, pady=10)

        # Image Display Area
        self.image_frame = tk.Frame(self.root, bg="#202020")
        self.image_frame.pack(expand=True, fill="both", pady=20)

        # Store image references
        self.image_labels = []
        self.image_paths = []

        # Display the selected files (Single Image Only)
        self.display_selected_images(file_paths)

    def add_single_file(self):
        """Allow adding a **single** image at a time"""
        file_path = select_file()
        if file_path:
            self.display_selected_images([file_path])  # Pass the single file as a list

    # def select_image(self, file_path, img_label):
    #     """Selects an image for watermarking and highlights it."""
    #     # Reset all previous selections
    #     for frame in self.image_labels:
    #         for widget in frame.winfo_children():
    #             widget.config(borderwidth=2, relief="flat")
    #
    #     # Highlight the selected image
    #     img_label.config(borderwidth=4, relief="solid", bg="blue")
    #
    #     # Store the selected image path
    #     self.selected_image_path = file_path
    #     self.next_step_button.config(state="normal")  # Enable the Next Step button

    def display_selected_images(self, file_paths):
        """Display a single image at a time"""
        try:
            for file_path in file_paths:
                self.image_paths.append(file_path)
                img = Image.open(file_path)
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)

                # Create a frame for the image and delete button
                img_frame = tk.Frame(self.image_frame, bg="#202020")
                img_frame.pack(side="left", padx=10, pady=10)

                # Display the image
                img_label = tk.Label(img_frame, image=photo, bg="#202020")
                img_label.image = photo
                img_label.pack()

                # Individual Delete Button for each image
                delete_button = tk.Button(
                    img_frame, text="❌", command=lambda p=file_path: self.delete_single_image(p),
                    font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat"
                )
                delete_button.pack(pady=5)

                # Save image data
                self.image_labels.append(img_frame)

            # Enable Clear Button when images are added
            self.clear_button.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def delete_single_image(self, file_path):
        """Delete an individual image"""
        for idx, img_frame in enumerate(self.image_labels):
            if self.image_paths[idx] == file_path:
                img_frame.destroy()
                self.image_labels.pop(idx)
                self.image_paths.pop(idx)
                break

        # Disable Clear Button if no images remain
        if not self.image_paths:
            self.clear_button.config(state="disabled")

    def clear_images(self):
        """Clear all images from the window"""
        for img_frame in self.image_labels:
            img_frame.destroy()
        self.image_labels.clear()
        self.image_paths.clear()
        self.clear_button.config(state="disabled")

    def next_step(self):
        # if not self.selected_image_path:
        #     messagebox.showwarning("Warning", "Please select an image before proceeding!")
        #     return

        """Transition to a new window with watermarking options, keeping buttons at the top."""
        # Hide the current content
        self.image_frame.pack_forget()
        self.top_bar.pack_forget()

        # New Window Layout (Watermarking Interface)
        self.watermark_frame = tk.Frame(self.root, bg="#202020")
        self.watermark_frame.pack(expand=True, fill="both")

        # ✅ TOP BAR Setup (All Buttons in a Row)
        self.bottom_bar = tk.Frame(self.root, bg="#303030", height=60)
        self.bottom_bar.pack(fill="x")

        # # Display the selected image in the watermark window
        # img = Image.open(self.selected_image_path)
        # img.thumbnail((500, 500))
        # self.processed_image = ImageTk.PhotoImage(img)

        # Back Button (Left Side)
        self.back_button = tk.Button(
            self.bottom_bar, text="Back", command=self.go_back_to_images,
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat"
        )
        self.back_button.pack(side="left", padx=5, pady=10)

        # Add Text Button (Center)
        self.add_text_button = tk.Button(
            self.bottom_bar, text="Add Text", command=lambda: self.apply_text_watermark(self.image_paths[-1]),
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat"
        )
        self.add_text_button.pack(side="left", padx=5, pady=10)

        # Add Logo Button (Center)
        self.add_logo_button = tk.Button(
            self.bottom_bar, text="Add Logo", command=lambda: self.apply_logo_watermark(self.image_paths[-1]),
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat"
        )
        self.add_logo_button.pack(side="left", padx=5, pady=10)

        # Remove Button (Disabled Initially)
        self.remove_button = tk.Button(
            self.bottom_bar, text="Remove", command=self.clear_images,
            font=("Arial", 12), bg="#3A3A3A", fg="white", relief="flat", state="disabled"
        )
        self.remove_button.pack(side="left", padx=5, pady=10)

        # Next Step Button (Right Side)
        self.next_step_button = tk.Button(
            self.bottom_bar, text="Next Step ➡️", command=self.next_step,
            font=("Arial", 12), bg="#4A90E2", fg="white", relief="flat"
        )
        self.next_step_button.pack(side="right", padx=5, pady=10)

        # Image Display Section (Below Top Bar)
        file_path = self.image_paths[-1]
        img = Image.open(file_path)
        img.thumbnail((500, 500))
        self.processed_image = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.watermark_frame, image=self.processed_image, bg="#202020")
        self.image_label.pack(pady=20)
    def go_home(self):
        """Return to the Home Window"""
        self.image_frame.pack_forget()
        self.top_bar.pack_forget()
        self.main_frame.pack(expand=True)
        self.footer_label.pack(side="bottom", pady=10)

    def go_back_to_images(self):
        """Properly return to the previous window with image display."""
        # Destroy the current watermarking window elements
        self.watermark_frame.pack_forget()
        self.bottom_bar.pack_forget()

        # Restore the previous window (image display)
        self.top_bar.pack(fill="x")
        self.image_frame.pack(expand=True, fill="both", pady=20)
