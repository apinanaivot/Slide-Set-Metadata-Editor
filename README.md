# Slide Set Metadata Editor

A simple GUI tool for batch editing metadata of image files, particularly useful for processing sets of slides.

## Features

- Open multiple image files (JPG, JPEG, PNG, TIF, TIFF)
- Set a single date for all opened images
  - Automatically increments time by 1 second for each image to maintain correct order when sorted by time
- Add and edit image titles/captions
- Copy titles to subsequent images
- Save metadata changes back to image files
- Thumbnail carousel for easy navigation
- Keyboard shortcuts for navigation (left/right arrow keys)

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- Pillow
- piexif

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries using pip:

```
pip install Pillow piexif
```

3. Download the `slide_set_metadata_editor.py` file from this repository.

## Usage

You can run the script in two ways:

1. Double-click the `slide_set_metadata_editor.py` file to launch the GUI directly.

2. Run from the command line:

```
python slide_set_metadata_editor.py
```

Once the application is running:

1. Click "Open Images" to select your slide images.
2. Use the date field and "Set Date" button to apply a date to all images.
   - The time will be set to noon (12:00:00) for the first image and increment by 1 second for each subsequent image.
3. Add captions in the title field and use "Copy & Next" to efficiently caption multiple slides.
4. Click "Save Changes" to apply all modifications.

## Note

This tool was created for personal use to streamline the process of adding metadata to sets of slides. It focuses on quick date setting and caption addition. As such, it may lack customization options or features that might seem obvious for more general use cases.

## Disclaimer

This tool modifies image files directly. Always work on copies of your original files.
