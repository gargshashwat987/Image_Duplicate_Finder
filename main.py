import tkinter as tk
import imagehash
import os
import openpyxl
from tkinter import filedialog
from PIL import Image, ImageTk
from collections import defaultdict
from tkinter import ttk
from PIL import UnidentifiedImageError
from datetime import datetime

def find_duplicate_images(folder_path, single_image_path):
    hash_dict = defaultdict(list)
    duplicate_path = ""
    if single_image_path:
        single_image_hash = calculate_dhash(single_image_path)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_dhash(file_path)
            if single_image_path and file_hash == single_image_hash:
                duplicate_path = file_path
                break
            hash_dict[file_hash].append(file_path)
    duplicates = hash_dict[single_image_hash] if single_image_path else hash_dict.get(single_image_hash, [])
    return duplicate_path, duplicates

def save_to_excel(file_path, duplicates):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Index', 'Path'])
    for i, duplicate_path in enumerate(duplicates, start=1):
        ws.append([i, duplicate_path])
    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"Duplicates_{date}.xlsx"
    full_path = os.path.join(file_path, filename)
    wb.save(full_path)

def browse_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_label_var.set(folder_path)

def browse_single_image():
    global single_image_path
    single_image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.ico *.jfif")])
    single_image_label_var.set(single_image_path)

def calculate_dhash(image_path):
    try:
        with Image.open(image_path) as img:
            return str(imagehash.dhash(img))
    except UnidentifiedImageError:
        return None

def process_image():
    if folder_path and single_image_path:
        single_image_hash = calculate_dhash(single_image_path)
        if single_image_hash is None:
            result_text.set("The selected single image is not a valid image file.")
            return
        duplicate_path, duplicates = find_duplicate_images(folder_path, single_image_path)
        if duplicate_path:
            result_text.set("Duplicate Image Found !")
            result_display.delete(*result_display.get_children())
            result_display.insert('', 'end', values=(1, duplicate_path))
            save_to_excel(folder_path, [duplicate_path])
        elif not duplicates:
            result_text.set("No Duplicate Image Found !")
        else:
            result_text.set("No Match Found !")
    else:
        result_text.set("Please select a folder and a single image before processing.")

root = tk.Tk()
root.title("Duplicate Image Finder")

logo_image = Image.open(r"D:\User Files\Downloads\path_infotech_ltd_logo.png")
logo_image = logo_image.resize((70, 70), Image.BOX)  # Adjust the size as needed
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo, bg='white')
logo_label.photo = logo_photo
logo_label.grid(row=0, column=0, columnspan=5,padx=5, pady=10, sticky="nw")

root.configure(bg='white')

style = ttk.Style()
style.configure("Colorful.TButton",
                background="black",
                foreground="black",
                padding=(5, 2))
style.map("Colorful.TButton",
          background=[('active', 'green')],
          foreground=[('active', 'blue')])
style.configure("Treeview",
                font=("Helvetica", 12),
                background="white",
                fieldbackground="white",
                foreground="black")

frame = tk.Frame(root, bg='white')
frame.grid(row=0,column=5,padx=50, pady=10,sticky='n')

title_label = tk.Label(frame, text="Duplicate Image Finder", font=("Helvetica", 20), bg='white',
                       fg='red')
title_label.grid(row=0, column=5,padx=5, pady=10,sticky='n')
title_label.pack()

folder_label_var = tk.StringVar()
folder_label_var.set("Select a folder")
folder_label = tk.Label(frame, textvariable=folder_label_var, bg='white', fg='red',
                        font=("Helvetica", 8))
folder_label.pack(pady=5, padx=5)

browse_folder_button = ttk.Button(frame, text="Browse Folder", command=browse_folder, style="Colorful.TButton")
browse_folder_button.pack(pady=10)

single_image_label_var = tk.StringVar()
single_image_label_var.set("Select a single image")
single_image_label = tk.Label(frame, textvariable=single_image_label_var, bg='white', fg='red',
                              font=("Helvetica", 8))
single_image_label.pack(pady=5, padx=5)

browse_single_image_button = ttk.Button(frame, text="Select Single Image", command=browse_single_image,
                                        style="Colorful.TButton")
browse_single_image_button.pack(pady=10)

process_button = ttk.Button(frame, text="Process Image", command=process_image, style="Colorful.TButton")
process_button.pack(pady=25, padx=25)

result_text = tk.StringVar()
result_text.set("")
result_label = tk.Label(frame, textvariable=result_text, bg='white', fg='red',
                        font=("Helvetica", 14))
result_label.pack()
result_display = ttk.Treeview(frame, columns=('Index', 'Path'), show='headings', height=15)
result_display.heading('Index', text='Index')
result_display.heading('Path', text='Path')
result_display.column('Index', width=60)
result_display.column('Path', width=600)
result_display.pack()

root.mainloop()
