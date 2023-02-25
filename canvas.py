import tkinter as tk
from PIL import ImageTk, ImageGrab
from pynput import keyboard
from threading import Thread
from logger import Logger as log

class CanvasWindow:
    def __init__(self, main_window, background_image):

        self.window = tk.Toplevel(main_window)
        self.window.config(cursor="crosshair")
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)
        self.window.geometry('0x0+0+0')
        self.screenshot = ImageTk.PhotoImage(background_image)
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill='both', expand=True)
        # Draw the screenshot on the Canvas
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.screenshot)
        self.img = ImageGrab.grab()
        # handle "escape" keyboard press in another thread
        keyboard_thread = Thread(target=self.start_keyboard)
        keyboard_thread.setDaemon(True)
        keyboard_thread.start()
        # Bind the mouse events to the Canvas
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None

        log.info("Canvas is ready to use.")
        # wait until this window is closed.After it is closed, the main window can continue processing
        main_window.wait_window(self.window)

    def start_keyboard(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        if key == keyboard.Key.esc:
            log.info("User pressed escape")
            self.window.destroy()

    def on_mouse_down(self, event):
        log.info("User clicked the mouse to draw...")
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                    outline="red")


    def on_mouse_drag(self, event):
        self.cur_x = self.canvas.canvasx(event.x)
        self.cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def on_mouse_up(self, event):
        log.info("User released the mouse.")
        # Grab the pixels within the rectangle and save them as a new image
        image = self.img.crop((int(self.start_x), int(self.start_y), int(self.cur_x), int(self.cur_y)))
        image.save("screenshot.png")
        log.info("Canvas window is being destroyed...")
        self.window.destroy()
