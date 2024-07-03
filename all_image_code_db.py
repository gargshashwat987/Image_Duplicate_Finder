import tkinter as tk                                    #for creating the GUI
import imagehash                                        #for generating image hashes
import os                                               #for working with file paths and directories
import openpyxl                                         #for working with Excel files
from tkinter import filedialog                          #for file and folder selection dialog
from PIL import Image, ImageTk                          #for image processing
from collections import defaultdict                     #for creating a dictionary with default values
from tkinter import ttk                                 #for themed Tkinter widgets
from PIL import UnidentifiedImageError
from datetime import datetime                           #for working with date and time

def calculate_dhash(image_path):
    with Image.open(image_path) as img:
        return str(imagehash.dhash(img))
    

def find_duplicate_images(folder_path):
    hash_dict = defaultdict(list)
    duplicates = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_dhash(file_path)
            hash_dict[file_hash].append(file_path)
    for hash_value, file_list in hash_dict.items():
        if len(file_list) > 1:
            duplicates.extend(file_list)
    return duplicates

def save_to_excel(file_path, duplicates):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Index', 'Path'])
    for i, duplicate_path in enumerate(duplicates, start=1):
        ws.append([i, duplicate_path])
    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Get the current date and time
    filename = f"Duplicates_{date}.xlsx"
    full_path = os.path.join(file_path, filename)
    wb.save(full_path)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        duplicates = find_duplicate_images(folder_path)
        if duplicates:
            result_text.set("Duplicate Images Found:")
            result_display.delete(*result_display.get_children())
            for i, duplicate_path in enumerate(duplicates, start=1):
                result_display.insert('', 'end', values=(i, duplicate_path))
            save_to_excel(folder_path, duplicates)  # Save the results to an Excel file with the current date and time
        else:
            result_text.set("No Duplicate Images Found")

root = tk.Tk()
root.title("Duplicate Image Finder")
root.configure(bg='white')

frame = tk.Frame(root, bg='white')
frame.pack(padx=10, pady=10)

title_label = tk.Label(frame, text="Duplicate Image Finder", font=("Helvetica", 20), bg='white')
title_label.pack()

browse_button = tk.Button(frame, text="Browse Folder", command=browse_folder, bg='red', fg='white', font=("Helvetica", 14))
browse_button.pack(pady=10)

result_text = tk.StringVar()
result_text.set("")
result_label = tk.Label(frame, textvariable=result_text, bg='white', font=("Helvetica", 14))
result_label.pack()

result_display = ttk.Treeview(frame, columns=('Index', 'Path'), show='headings', height=10)
result_display.heading('Index', text='Index')
result_display.heading('Path', text='Path')
result_display.column('Index', width=50)
result_display.column('Path', width=600)  # Width of output box
result_display.pack()

style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12))

root.mainloop()