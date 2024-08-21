import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import piexif

class ImageMetadataGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Metadata Editor")
        master.geometry("1024x768")

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Top frame for buttons
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        # Open images button
        self.open_button = ttk.Button(top_frame, text="Open Images", command=self.open_images)
        self.open_button.pack(side=tk.LEFT, padx=5)

        # Close images button
        self.close_button = ttk.Button(top_frame, text="Close Images", command=self.close_images)
        self.close_button.pack(side=tk.LEFT, padx=5)

        # Date entry and set date button
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(top_frame, width=10, textvariable=self.date_var)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        self.date_entry.insert(0, "dd/mm/yyyy")
        self.date_entry.bind("<FocusIn>", self.clear_date_placeholder)
        self.date_entry.bind("<FocusOut>", self.restore_date_placeholder)

        self.set_date_button = ttk.Button(top_frame, text="Set Date", command=self.set_date)
        self.set_date_button.pack(side=tk.LEFT, padx=5)

        # Save changes button
        self.save_button = ttk.Button(top_frame, text="Save Changes", command=self.save_changes)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # Middle frame for image display
        self.image_frame = ttk.Frame(self.main_frame, height=400)
        self.image_frame.pack(fill=tk.X, padx=5, pady=5)
        self.image_frame.pack_propagate(False)  # Prevent the frame from shrinking
        self.current_image_label = ttk.Label(self.image_frame)
        self.current_image_label.pack(fill=tk.BOTH, expand=True)

        # Bottom frame for title entry and thumbnail carousel
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Title entry
        title_frame = ttk.Frame(self.bottom_frame)
        title_frame.pack(fill=tk.X, pady=5)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, width=50, textvariable=self.title_var)
        self.title_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Copy title button
        self.copy_title_button = ttk.Button(title_frame, text="Copy & Next", command=self.copy_title_and_next)
        self.copy_title_button.pack(side=tk.LEFT, padx=5)

        # Thumbnail carousel
        self.carousel_frame = ttk.Frame(self.bottom_frame)
        self.carousel_frame.pack(fill=tk.X, expand=True)
        
        # Set fixed width for carousel (9 thumbnails * 100 pixels each)
        carousel_width = 9 * 100
        self.carousel_canvas = tk.Canvas(self.carousel_frame, height=120, width=carousel_width)
        self.carousel_canvas.pack(side=tk.LEFT)
        
        self.carousel_scrollbar = ttk.Scrollbar(self.carousel_frame, orient="horizontal", command=self.carousel_canvas.xview)
        self.carousel_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)
        self.carousel_canvas.configure(xscrollcommand=self.carousel_scrollbar.set)

        # Bind arrow keys
        master.bind('<Left>', self.prev_image)
        master.bind('<Right>', self.next_image)

        self.images = []
        self.current_index = 0
        self.thumbnails = []
        self.image_titles = {}
        self.thumbnail_buttons = []

    def clear_date_placeholder(self, event):
        if self.date_var.get() == "dd/mm/yyyy":
            self.date_var.set("")

    def restore_date_placeholder(self, event):
        if self.date_var.get() == "":
            self.date_var.set("dd/mm/yyyy")

    def open_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.tif *.tiff")])
        self.images = list(file_paths)
        self.current_index = 0
        self.image_titles = {img: self.get_image_title(img) for img in self.images}
        self.update_thumbnail_carousel()
        self.show_current_image()

    def close_images(self):
        self.images = []
        self.current_index = 0
        self.image_titles.clear()
        self.title_var.set("")
        self.current_image_label.config(image="")
        self.update_thumbnail_carousel()

    def get_image_title(self, img_path):
        try:
            exif_dict = piexif.load(img_path)
            title = exif_dict.get('0th', {}).get(piexif.ImageIFD.ImageDescription, b'').decode('utf-8')
            return title
        except:
            return ''

    def update_thumbnail_carousel(self):
        for widget in self.carousel_canvas.winfo_children():
            widget.destroy()
        self.thumbnails = []
        self.thumbnail_buttons = []

        for i, img_path in enumerate(self.images):
            img = Image.open(img_path)
            img.thumbnail((90, 120))  # 3:4 aspect ratio
            photo = ImageTk.PhotoImage(img)
            self.thumbnails.append(photo)
            
            button = tk.Button(self.carousel_canvas, image=photo, command=lambda idx=i: self.show_image(idx))
            self.thumbnail_buttons.append(button)
            self.carousel_canvas.create_window(i*100 + 50, 60, window=button)

        self.carousel_canvas.config(scrollregion=self.carousel_canvas.bbox("all"))
        self.highlight_selected_thumbnail()

    def show_current_image(self):
        self.show_image(self.current_index)

    def show_image(self, index):
        if 0 <= index < len(self.images):
            self.update_current_image_title()
            self.current_index = index
            img = Image.open(self.images[self.current_index])
            
            # Resize image to fit within 400 pixels height while maintaining aspect ratio
            img.thumbnail((self.image_frame.winfo_width(), 400))
            
            photo = ImageTk.PhotoImage(img)
            self.current_image_label.config(image=photo)
            self.current_image_label.image = photo
            self.title_var.set(self.image_titles[self.images[self.current_index]])
            
            self.center_carousel()
            self.highlight_selected_thumbnail()

    def highlight_selected_thumbnail(self):
        for i, button in enumerate(self.thumbnail_buttons):
            if i == self.current_index:
                button.config(borderwidth=3, relief="raised")
            else:
                button.config(borderwidth=1, relief="flat")

    def center_carousel(self):
        if not self.images:
            return
        
        canvas_width = self.carousel_canvas.winfo_width()
        item_width = 100  # Width of each thumbnail item
        
        # Calculate the scroll position to center the current item
        scroll_pos = (self.current_index * item_width) - (canvas_width / 2) + (item_width / 2)
        
        # Ensure scroll_pos is within bounds
        max_scroll = self.carousel_canvas.bbox("all")[2] - canvas_width
        scroll_pos = max(0, min(scroll_pos, max_scroll))
        
        # Move the canvas
        self.carousel_canvas.xview_moveto(scroll_pos / self.carousel_canvas.bbox("all")[2])

    def update_current_image_title(self):
        if self.images:
            current_image = self.images[self.current_index]
            self.image_titles[current_image] = self.title_var.get()

    def copy_title_and_next(self):
        if self.current_index < len(self.images) - 1:
            current_title = self.title_var.get()
            self.update_current_image_title()
            self.current_index += 1
            self.image_titles[self.images[self.current_index]] = current_title
            self.show_current_image()

    def set_date(self):
        date_string = self.date_var.get()
        try:
            selected_date = datetime.strptime(date_string, "%d/%m/%Y")
            for i, img_path in enumerate(self.images):
                try:
                    exif_dict = piexif.load(img_path)
                    date_time = selected_date.replace(hour=12, minute=0, second=i)  # Set time to noon and increment seconds
                    date_string = date_time.strftime("%Y:%m:%d %H:%M:%S")
                    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_string
                    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_string
                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, img_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to set date for {os.path.basename(img_path)}: {str(e)}")
            messagebox.showinfo("Success", "Date set for all images.")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use dd/mm/yyyy.")

    def save_changes(self):
        self.update_current_image_title()
        for img_path, title in self.image_titles.items():
            try:
                exif_dict = piexif.load(img_path)
                exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, img_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save title for {os.path.basename(img_path)}: {str(e)}")
        messagebox.showinfo("Success", "Changes saved for all images.")

    def prev_image(self, event):
        if self.current_index > 0:
            self.update_current_image_title()
            self.current_index -= 1
            self.show_current_image()

    def next_image(self, event):
        if self.current_index < len(self.images) - 1:
            self.update_current_image_title()
            self.current_index += 1
            self.show_current_image()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageMetadataGUI(root)
    root.mainloop()