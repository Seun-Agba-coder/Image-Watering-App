import tkinter as tk
from tkinter import ttk
class SaveImage(tk.Toplevel):
    def __init__(self, master, image):
        super().__init__(master)
        self.geometry("220x300+700+100")
        self.resizable(False, False)
        self.image = image


        self.file_format = tk.Label(self, text="file format: ", font=("Times New Roman", 10))
        self.file_format.grid(row=1, column=0, pady=10)
        self.string_var = tk.StringVar()
        self.string_var.set("Original Format")
        self.string_var.trace("w", self.save_image)
        self.formatchosen = ttk.Combobox(self, width=27,
                                    textvariable=self.string_var)
        self.formatchosen.grid(row=2, column=0, pady=10)
        self.formatchosen["values"] = (
            "Original Format",
            "Convert to JPEG",
            "Convert to PNG",
            "Convert to WEBP"
        )

    def save_image(self, *args):
        if self.string_var.get() == "Convert to JPEG":
            self.image.save("first image.jpeg")


