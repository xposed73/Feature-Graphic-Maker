import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinter import ttk
from PIL import Image, ImageDraw, ImageOps, ImageTk
from colorthief import ColorThief
from ttkthemes import ThemedTk

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Generator")

        # Set a modern theme
        self.style = ttk.Style()
        self.style.theme_use('clearlooks')  # Choose other themes like 'breeze', 'clam', etc.

        # Icon selection
        self.icon_path = ""
        self.background_color = (255, 255, 255)  # Default white

        # Create GUI elements
        self.create_widgets()
        self.update_window_size()

    def create_widgets(self):
        # Create frames for layout
        frame_icon = ttk.Frame(self.root, padding="10")
        frame_color = ttk.Frame(self.root, padding="10")

        # Icon selection
        ttk.Label(frame_icon, text="Choose an icon:").pack(pady=5)
        self.icon_button = ttk.Button(frame_icon, text="Browse", command=self.choose_icon)
        self.icon_button.pack(pady=5)

        # Background color
        ttk.Label(frame_color, text="Choose background color:").pack(pady=5)
        self.bg_color_button = ttk.Button(frame_color, text="Choose Color", command=self.choose_color)
        self.bg_color_button.pack(pady=5)
        ttk.Button(frame_color, text="Auto Color", command=self.auto_color).pack(pady=5)

        # Pack frames
        frame_icon.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        frame_color.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        # Generate button
        ttk.Button(self.root, text="Generate Image", command=self.generate_image).grid(row=2, column=0, pady=20)

        # Adjust the column weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def update_window_size(self):
        # Auto-size the window to fit content
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.root.geometry(f"{width}x{height}")

    def choose_icon(self):
        self.icon_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.icon_path:
            # Optionally update UI or show the chosen icon
            pass

    def choose_color(self):
        color = colorchooser.askcolor()[0]
        if color:
            self.background_color = tuple(map(int, color))

    def auto_color(self):
        if not self.icon_path:
            messagebox.showerror("Error", "Please choose an icon first.")
            return
        color_thief = ColorThief(self.icon_path)
        self.background_color = color_thief.get_color(quality=1)

    def generate_image(self):
        if not self.icon_path:
            messagebox.showerror("Error", "Please choose an icon first.")
            return

        width, height = 1024, 500
        icon_size = 300
        corner_radius = 20

        icon = Image.open(self.icon_path)
        icon = icon.resize((icon_size, icon_size), Image.LANCZOS)

        image = Image.new('RGB', (width, height), self.background_color)

        mask = Image.new('L', (icon_size, icon_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, icon_size, icon_size], radius=corner_radius, fill=255)

        rounded_icon = ImageOps.fit(icon, (icon_size, icon_size), centering=(0.5, 0.5))
        rounded_icon.putalpha(mask)

        icon_position = ((width - icon_size) // 2, (height - icon_size) // 2)
        image.paste(rounded_icon, icon_position, rounded_icon)

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            image.save(output_path)
            print(f"Image saved to {output_path}")
            image.show()

if __name__ == "__main__":
    root = ThemedTk()  # Use ThemedTk to apply a modern theme
    app = ImageGeneratorApp(root)
    root.mainloop()
