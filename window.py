import canvas
import os
import pyperclip
import pytesseract
import shutil
import time
import tkinter as tk
from threading import Thread
from tkinter import ttk, filedialog
from configurator import Config
from logger import Logger as log

from PIL import ImageGrab, Image


class MainWindow:
    def __init__(self):
        self.button_capture = None
        self.button_save = None
        self.button_ocr = None
        self.label_status = None
        self.window = tk.Tk()
        self.window.title('Capture')
        self.window.resizable(False, False)
        self.center_screen(200, 100)
        self.background_color = '#E0E0E0'
        self.window.configure(bg=self.background_color)
        self.create_elements()
        self.tesseract_engine = Config.read("CONSTANTS", "tesseract_path")
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_engine # r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.button_ocr["state"] = "disabled"
        self.button_save["state"] = "disabled"
        log.info("Main window is ready to use.")
        self.window.mainloop()

    def center_screen(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x_coordinate, y_coordinate))

    def create_elements(self):
        self.button_capture = ttk.Button(self.window, text='+', command=self.button_capture_onclick)
        self.button_capture.place(x=20, y=20, width=40, height=40)

        self.button_save = ttk.Button(self.window, text='save', command=self.button_save_onclick)
        self.button_save.place(x=80, y=20, width=40, height=40)

        self.button_ocr = ttk.Button(self.window, text='ocr', command=self.button_ocr_onclick)
        self.button_ocr.place(x=140, y=20, width=40, height=40)

        self.label_status = ttk.Label(self.window, text="Ready.", background=self.background_color)
        self.label_status.place(x=20, y=70)

    def button_capture_onclick(self):
        # delete existing screenshot
        if os.path.exists("screenshot.png"):
            os.remove("screenshot.png")
        # update label text
        self.label_status["text"] = "Screenshot is being taken..."
        log.info("Screenshot is being taken...")
        # hide the main program
        self.window.withdraw()
        time.sleep(1)
        # take the screenshot
        ss = ImageGrab.grab()
        # create the canvas
        log.info("Canvas is being created...")
        canvas.CanvasWindow(self.window, ss)
        log.info("Canvas has been terminated.")
        self.window.deiconify()
        self.window.update()
        log.info("Main window is active again.")
        # if there is ss, enable ocr button
        if os.path.exists("screenshot.png"):
            log.info("Screenshot has been taken successfully.")
            self.button_ocr["state"] = "enabled"
            self.button_save["state"] = "enabled"
            self.label_status["text"] = "Image grabbed successfully"
        else:
            log.info("Taking screenshot has been cancelled by the user.")
            self.label_status["text"] = "Cancelled"
            time.sleep(1)
            self.label_status["text"] = "Ready."

    def button_ocr_onclick(self):
        if self.tesseract_engine == "":
            self.label_status["text"] = "Tesseract engine not found!"
            log.warn("OCR Engine not found")
            te_file = filedialog.askopenfilename(defaultextension='.exe', title='Choose Tesseract Engine')
            if te_file:
                log.info("OCR engine selected : " + te_file)
                Config.edit("CONSTANTS", "tesseract_path", te_file)
                self.tesseract_engine = te_file
                pytesseract.pytesseract.tesseract_cmd = te_file
            else:
                log.info("OCR engine selection cancelled.")
                self.label_status["text"] = "OCR engine selection cancelled."
                time.sleep(1)
                self.label_status["text"] = "Ready."
                return
        self.button_ocr["state"] = "disabled"
        self.button_capture["state"] = "disabled"
        ocr = Thread(target=self.run_ocr)
        ocr.setDaemon(True)
        ocr.start()

    def run_ocr(self):
        try:
            log.info("OCR Engine will select the screenshot")
            img = Image.open("screenshot.png")

        except FileNotFoundError:
            log.error("Screenshot.png file not found.")
            self.label_status["text"] = "Screenshot.png not found!"
            self.button_ocr["state"] = "enabled"
            self.button_capture["state"] = "enabled"
            self.label_status["text"] = "Ready."
            return

        text = pytesseract.image_to_string(img)
        log.info("Screenshot has been converted to text")
        pyperclip.copy(text)
        log.info("Text has been copied to clipboard")
        self.label_status["text"] = "Copied to clipboard"
        self.button_ocr["state"] = "enabled"
        self.button_capture["state"] = "enabled"
        time.sleep(1)
        self.label_status["text"] = "Ready."

    def button_save_onclick(self):
        log.info("Screenshot will be saved...")
        file_path = filedialog.asksaveasfilename(defaultextension='.png')
        if file_path:
            # copy file
            shutil.copy2("screenshot.png", file_path)
            log.info("Screenshot has been copied to " + file_path)
            self.label_status["text"] = "Copied to the destination."
        else:
            log.info("Saving screenshot has been cancelled by the user")
