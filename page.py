from tkinter import ttk, filedialog, font
import tkinter as tk
from ttkbootstrap import Style
from PIL import ImageTk, Image
import numpy as np
from editing_page import Window3


class Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self["padding"] = 15, 6
        self.grid()


        # create canvas
        self.canvas = tk.Canvas(self, height=400, width=400, bg="#E4E4E4")

        self.canvas.grid(row=1, column=0, pady=50)
        # opens the image of the waterlogo in the images file
        self.img = Image.open("./images/Water mark logo.png")

        # resizes the image
        resized_image = self.img.resize((60, 60), resample=3)
        self.image = ImageTk.PhotoImage(image=resized_image)


        self.canvas.create_text(195, 190, text="Add Watermark", fill="blue", font=("Brush", 20, 'bold'))
        # Adds image to the canvas
        self.canvas.create_image(190, 130, image=self.image)
        self.file_button = tk.Button(self.canvas,
                                     text="Select File",
                                     activebackground="red",
                                     font=("Times New Roman", 10, "italic"),
                                     highlightcolor="red",
                                     command=self.select_file, foreground="blue")
        self.canvas.create_window(159, 225, anchor="nw", window=self.file_button)



        # creates a sort of navbar
        style = Style()
        style.configure("custom.TFrame", background="skyblue")
        self.second_frame = ttk.Frame(self,style='custom.TFrame', height=50,  width=860)
        self.second_frame.grid(row=0, column=0, padx=10, pady=5,)
        self.close_app_button = ttk.Button(self.second_frame,
                                           text="Close Application",
                                           command=self.quit,
                                           style="Kim.TButton",
                                           )
        self.close_app_button.place(x=10, y=10)

        self.select_file_button = ttk.Button(self.second_frame,
                                      text="Select File",
                                      style="Kim.TButton", command=self.select_file)
        self.select_file_button.place(x=375, y=10)


    def select_file(self):
        """Selects image from the filedialog box"""
        # selects image from a folder
        file_name = filedialog.askopenfilename(initialdir="/C:/Users/HP/Downloads",
                                               title="Select Image File",
                                               parent=self.master,
                                               filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif'))
        )
        print(file_name)
        if len(file_name) == 0:
            pass
        else:
            Window2(self, file_name)




class Window2(tk.Toplevel):
    def __init__(self, master, file_name):
        super().__init__(master)
        self.geometry('900x600+300+100')
        self.resizable(False, False)
        self.config(padx=10, pady=7)
        # # initializes the ttkinter sytle class
        # style = Style()
        # style.configure(self.)
        # image chosen by user
        self.image = None


        # behaves like a nav bar
        style = Style()
        style.configure('color.TFrame', background="purple")
        self.top_frame = ttk.Frame(self, height=50, width=850, style="color.TFrame")
        self.top_frame.grid(row=0, column=0, padx=5, pady=0, sticky="W")

        ## Destroys the current window
        self.back_button = ttk.Button(self.top_frame, text="Back", command=self.destroy, width=7, style="danger.Outline.TButton")
        self.back_button.place(x=20, y=12)

        # Add new files to the window
        self.add_files = tk.Button(self.top_frame,
                                   text="Add Files", width=7, state=tk.NORMAL,
                                   command=lambda : self.show_images_class(filename=self.Add_file()))


        self.add_files.place(x=425, y=12)

        # Takes User to the next window
        # Styles the button
        style.configure("success.Outline.TButton",
                        font=("Comic Sans Ms" ,7, "bold"),
                        )
        self.next_step_button = ttk.Button(self.top_frame,
                                   text="Next Step",
                                    style="success.Outline.TButton",
                                    command=self.create_window3_instace)

        self.next_step_button.place(x=770, y=12)

        # if self.back_button pressed remember to show a prompt before deleting


        # self.first_image = ShowImage(master=self, filename=file_name)
        # self.image_instances_list.append(self.first_image)
        self.showimage(file_name=file_name)




    def showimage(self, file_name):
        global img1

        with Image.open(file_name) as img:
            # inserts the attribute above with the image open
            self.image = img
            # Resizes the image
            resized_img = self.image.resize((200, 155), resample=3)


            img1 = ImageTk.PhotoImage(resized_img)
            label = tk.Label(self, image=img1)
            style = ttk.Style()
            style.configure("TButton", foreground="red")
            delete_button = ttk.Button(self,
                                       text="delete",
                                       style="danger.Outline.TButton",
                                       command=lambda: [label.destroy(),
                                                        delete_button.destroy(), self.check_image_deleted()])
            label.grid(row=1, column=0, sticky='W', padx=10, pady=11)
            delete_button.grid(row=2, column=0, sticky="W", padx=10,)


    def check_image_deleted(self):
        """If image is delted Next step button is disabled"""
        self.next_step_button["state"] = tk.DISABLED




    def Add_file(self):
        # Adds new files to the window
        # selects image from a folder

        file_name = filedialog.askopenfilename(initialdir="/C:/Users/HP/Downloads",
                                               title="Select Image File",
                                               parent=self)

        return file_name


    def create_window3_instace(self):
        Window3(self, self.image)
