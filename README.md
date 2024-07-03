# Duplicate_Image_Finder

The Duplicate Image Finder application is designed to assist users in identifying and managing duplicate images within a specified folder. The application can handle certain file types like JPG, JPEG, PNG, GIF, BMP, TIFF, ICO or JFIF. It has been created using Python programming language and the tkinter library for the graphic user interface (GUI). It allows users to: 
1.	Select a target folder.
2.	choose a single image for comparison.
3.	find duplicates of selected image within the specified folder.
4.	display the duplicate images found in a user-friendly format.
5.	save the results in an excel file.

The application incorporates the following key features:
1.	Browse Folder: users can select a folder containing images they want to search for duplicates in.
2.	Select a single image: users can choose a single image to compare against the images in the selected folder.
3.	Process image: this button initiates the comparison process finding and displaying any duplicate images and allowing for the results to be saved in an excel file.
4.	Result display: the application provides a table that displays the index and file path of the found duplicate images.

The application relies on the following Python libraries:
•	Tkinter
•	Imagehash
•	Openpyxl
•	Pillow
•	Collections
•	Datetime
