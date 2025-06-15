Image to PDF Converter 
- This is a simple web app built with Flask that allows users to upload multiple `.png`, `.jpg`, or `.jpeg` images and generate a print-ready PDF file. Images are resized and centered to fit A4 pages using `reportlab`.

Features
- Upload multiple images at once
- Automatic A4 fitting & centering
- Clean PDF export
- In-memory processing & cleanup

Tech Stack
- Python 3
- Flask
- Pillow (image processing)
- ReportLab (PDF generation)

Requirements
- Flask
- Pillow
- reportlab

Output
- All uploaded images are stored temporarily and cleaned up after PDF generation. The generated PDF is saved in the output/ folder and offered as a downloadable file.

Screenshot
![image](https://github.com/user-attachments/assets/1864d6b2-4758-4919-b1e4-04356a5f7c5b)
