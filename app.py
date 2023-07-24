import tkinter as tk
from tkinter import filedialog
from process import process_pdf
import os

def upload_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    if not filepath.lower().endswith('.pdf'):
        print('Error: Only PDF files are supported.')
        return
    filesize = os.path.getsize(filepath)
    if filesize > 50 * 1024 * 1024:
        print('Error: File size must be 50 MB or less.')
        return
    success, message = process_pdf(filepath)
    if success:
        print('Success: ', message)
    else:
        print('Error: ', message)

def main():
    window = tk.Tk()
    label = tk.Label(window, text="Select a file you want to scan (max size 50Mb)")
    label.pack()
    window.geometry("500x500")
    window.title("ScanMyPDF")
    upload_button = tk.Button(window, text='Upload PDF', command=upload_file)
    upload_button.pack()
    window.mainloop()

if __name__ == '__main__':
    main()
