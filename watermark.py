from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox

from PIL._tkinter_finder import tk


def add_watermark(image_path, window):
    try:
        img = Image.open(image_path)
        watermark_text = "Watermark"

        # Add watermark
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)

        # Position the watermark at the bottom-right corner
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        position = (img.width - text_width - 10, img.height - text_height - 10)

        draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)
        img.save("watermarked_image.png")

        # Show success message
        messagebox.showinfo("Success", "Watermark added successfully!")

        # Refresh the window with the new watermarked images
        img.thumbnail((300, 300))
        watermarked_display = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=watermarked_display)
        label.image = watermarked_display
        label.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
