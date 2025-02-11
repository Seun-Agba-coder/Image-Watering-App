import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from ttkbootstrap import Style
from ttkbootstrap.dialogs.dialogs import FontDialog
import numpy
from PIL import Image, ImageTk
from save_watermark import SaveImage
import math


class Window3(tk.Toplevel):
    def __init__(self, master, image):
        super().__init__(master)
        # getting screen width and height of display
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        print(f"The height of my screen is {self.height} while the width is {self.width}")
        # setting tkinter window size to occupy full size of user screen
        self.geometry("%dx%d" % (self.width, self.height))
        self.config(padx=10, pady=3)
        # stores the image parameter into an attribute
        self.image = image

        #creates a nav bar
        self.frame_width = self.width - 40
        self.nav_bar_frame= ttk.Frame(self, height=50, width=self.frame_width, style="secondary.TFrame",)
        self.nav_bar_frame.grid(row=0, column=0)
        style = Style()
        style.configure("danger.Outline.TButton", font=("Georgia", 12, "bold"))
        self.back_button = ttk.Button(self.nav_bar_frame,
                                     text="Back",
                                     command=self.destroy,
                                    style="danger.Outline.TButton"
                                     )
        # This button helps add text to the image
        self.add_text = tk.Button(self.nav_bar_frame,
                                  text="Add Text",
                                  fg="blue",
                                  command=self.text_box, font=("Georgia", 12, "bold"))
        #This Button helps add logo to the image
        self.add_logo = tk.Button(self.nav_bar_frame,
                                  text="Add Logo",
                                  fg="blue",
                                  command=self.place_img, font=("Georgia", 12, "bold"))

        self.save_image = ttk.Button(self.nav_bar_frame,
                                  text="Save Image",
                                  command=self.save_image, style="success.Outline.TButton.")

        self.back_button.place(x=self.frame_width /12 -30, y=12)
        self.add_text.place(x=self.frame_width /2 -200 , y=15)
        self.add_logo.place(x=self.frame_width /2 +100, y=15)
        self.save_image.place(x=self.frame_width-100,  y=15)

        # Gets the text written in the entry widget
        self.entry_widget_text = None
        # gets initial Text ment to be written on the image

        #Gets the width and heigth of the image
        self.img_width = self.image.width
        self.img_height = self.image.height

        # checks if the img_height of the image is above the screen limit then resizes it by shrinking the image by half
        if self.img_height > self.height:
            print("True")
            self.img_width = int(self.img_width / 2)
            self.img_height = int(self.img_height / 2)
            image = self.image.resize((self.img_width, self.img_height))

        else:
            pass

        print(f"This image has a img_height of {self.img_height}, and a img_width of {self.img_width}")
        self.canvas = tk.Canvas(self, height=image.height, width=image.width, bg="blue")
        self.canvas.grid(row=1, column=0, pady=40)
        self.img = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.img)
        #self.editing_text = self.canvas.create_text(self.img_width/2, self.img_height/2, text=f"", font=("New Times Roman", 15, "bold"))



        #keeps track of the amount of times the text box function is clicked
        self.num = 0



        self.text_boxes: list = []
        self.image_boxes: list  = []


    def text_box(self):
        # Frame for textbox
        image_text = ImageText(master=self, canvas=self.canvas, height=self.img_height, width=self.img_width)

        self.text_boxes.append(image_text)
        if len(self.text_boxes) != 1:
            self.text_boxes[self.num].text_box_frame.destroy()
            self.num +=1





    def place_img(self):
        """Places the image on the canvas"""
        file_name = filedialog.askopenfilename(initialdir="/C:/Users/HP/Downloads",
                                               title="Select Image File",
                                               parent=self)

        image = CanvasImage(master=self, canvas=self.canvas, width=self.img_width, height=self.img_height)
        image.place_img(file_name)
        self.image_boxes.append(image)







    def save_image(self):
        """Saves the watermarked image"""
        print(self.image)
        print(self.image)
        SaveImage(master=self, image=self.image)





class ImageText:

    def __init__(self, master, canvas, height, width):
        self.canvas = canvas
        self.height = height
        self.width = width
        self.editing_text = self.canvas.create_text(self.width / 2, self.height / 2, text=f"",
                                                    font=("New Times Roman", 15, "bold"))
        self.master = master
        self.canvas.tag_bind(self.editing_text, '<B1-Motion>', lambda e: self.move_text_anywhere_on_image(e.x, e.y))
        self.canvas.tag_bind(self.editing_text, '<Button-1>', lambda e: self.clicked_text_box())
        self.text_box_frame = None
        self.text_box(master=self.master,  click=1)
        self.color_code = None
    def text_box(self, master, click, text=None):
        self.text_box_frame = ttk.Frame(
            master, height=600, width=400, )
        self.text_box_frame.grid(row=1, column=0, sticky="NW", )

        # Text box title
        self.title_label = ttk.Label(self.text_box_frame, text="Properties")
        self.title_label.grid(row=0, column=0, pady=5)

        # Opens the exit in the images folder and resizes it for it to be able to fit the button
        with Image.open("./images/exit img.png") as img:
            resized_image = img.resize((15, 15), resample=3)

        self.exit_image = ImageTk.PhotoImage(resized_image)
        # button to destroy the textbox frame
        self.exit_button = ttk.Button(self.text_box_frame, image=self.exit_image,
                                      command=self.text_box_frame.destroy)
        self.exit_button.grid(row=0, column=1)

        # Creates an instance of the StringVar object
        if click == 1:
            self.text_var = tk.StringVar(master, "Write Your Text")
        else:
            self.text_var = tk.StringVar(master, text)
        # inserts a text into the image once the text_box function is called
        self.canvas.itemconfig(self.editing_text, text=f"{self.text_var.get()}", fill="white")
        # checks if the self.text_var variable or instance is being changed ("write") if so calls back a function
        # to update the text on the image
        self.text_var.trace("w", self.change_text_on_image)

        # label to show the user to write text in the entry box
        label = ttk.Label(self.text_box_frame, text="Write Text", font=("New Times Roman", 10, "bold"))
        label.grid(row=1, column=0, sticky="W", pady=3)

        self.entry_box = ttk.Entry(self.text_box_frame, textvariable=self.text_var, width=40, )
        self.entry_box.grid(row=2, column=0, sticky="W")

        # # Create an instance of the intvar object
        # self.int_var = tk.IntVar()
        # # Sets the initial value for the intvar
        # self.int_var.set(15)
        # self.int_var.trace("w", self.change_text_on_image)
        #
        # # label to keep track of font size of the image
        # self.scale_label = tk.Label(self.text_box_frame, text=f"Font Size of Text: {self.int_var.get()}",
        #                             foreground="#F0C38B", font=("New Times Roman", 15, "bold"))
        # self.scale_label.grid(row=3, column=0, sticky="W")
        # # used to increase the font size of the text
        # font_size_scale_widget = ttk.Scale(self.text_box_frame,
        #                                    from_=1,
        #                                    to=50,
        #                                    orient=tk.HORIZONTAL,
        #                                    variable=self.int_var, length=200)
        # font_size_scale_widget.grid(row=4, column=0, sticky="W")

        # button to help  display a dialog to change the current font style and size
        self.font_dialog = tk.Button(self.text_box_frame,
                                     text="Change Font Size and Style",
                                     anchor="w",
                                     width=35,
                                     command=lambda: self.show_different_fonts_available(
                                         master=self.text_box_frame))
        self.font_dialog.grid(row=6, column=0, )

        self.change_color = tk.Button(self.text_box_frame,
                                      text="Change Font Color",
                                      anchor="w",
                                      width=35,
                                      command=lambda: self.change_font_color(self.text_box_frame))
        self.change_color.grid(row=7, column=0)

        self.float_var = tk.DoubleVar()
        self.float_var.set(0)
        self.float_var.trace('w', self.rotate_text)

        # keeps track of the rotation of the text
        self.rotation_label = tk.Label(self.text_box_frame, text=f"Rotation: {self.float_var.get()}")
        self.rotation_label.grid(row=8, column=0, sticky="W")

        # Scale widget for rotation of text
        rotation_scale_widget = ttk.Scale(self.text_box_frame,
                                          from_=-180,
                                          to=180,
                                          orient=tk.HORIZONTAL,
                                          variable=self.float_var, length=200)
        rotation_scale_widget.grid(row=9, column=0, sticky="W")

        # image for the trashcan
        with Image.open("./images/trashcan-icon-5315275.jpg") as delete_image:
            resized_delete_image = delete_image.resize((20, 21), resample=3)
            self.delete_image = ImageTk.PhotoImage(resized_delete_image)
        # deletes both the image text and destroys the frame
        delete_button = ttk.Button(self.text_box_frame, image=self.delete_image, style="danger.TButton", command=self.delete_current_text)
        delete_button.grid(row=10, column=1)
        delete_text = ttk.Label(self.text_box_frame, text="delete")
        delete_text.grid(row=11, column=1)



        # Sets the padding for all the widget contained on this frame simultaneously
        count = 0
        for widget in self.text_box_frame.winfo_children():
            if count == 1 or count == 2 or count == 0 or count == 7 or count == 8 or count == 10:
                pass
            else:
                widget.grid(padx=5, pady=17)
            count += 1

    def clicked_text_box(self, *args):
        """destroys the previous text box frame and places the new one fro when the text is clicked"""
        entry_widget_text = self.text_var.get()

        self.text_box_frame.destroy()
        self.text_box(master=self.master, text=entry_widget_text, click=2)
        fill = self.color_code
        if fill is None:
            fill = "white"
        else:
            fill = fill[1]
        self.canvas.itemconfig(self.editing_text, fill=fill)

    def move_text_anywhere_on_image(self, x, y):
        """This function moves the text anywhere on the image"""
        if y in range(0, self.height-20) and x in range(0, self.width-20):
            self.canvas.moveto(self.editing_text, x, y)



    def change_text_on_image(self, *args, ):
        """Basically changes the text on the image"""
        self.canvas.itemconfig(self.editing_text,
                               text=f"{self.text_var.get()}",
                               )



    def show_different_fonts_available(self, master):
        """Shows the different fonts available on the system and allow for any to be chosen and used"""

        # Define Font Dialog
        fd = FontDialog(parent=master)
        # Show the box
        fd.show()
        # Capture The Reult fd.result and update label
        if fd.result:
            self.canvas.itemconfig(self.editing_text,
                                   font=fd.result)
        else:
            pass

    def change_font_color(self, master):
        """Changes the font color of the text written on the image"""
        self.color_code = colorchooser.askcolor(title="Choose color", parent=master)
        print(self.color_code)
        if None not in self.color_code:
            print()
            self.canvas.itemconfig(self.editing_text, fill=f"{self.color_code[1]}")
        else:
            pass

    def rotate_text(self, *args):
        """rotate angle with the normal scale"""
        self.canvas.itemconfig(self.editing_text, angle=self.float_var.get())
        self.rotation_label.configure(text=f"Rotation: {int(self.float_var.get())}")

    def delete_current_text(self):
        """deletes the current text"""
        self.text_box_frame.destroy()
        self.canvas.delete(self.editing_text)






class CanvasImage:
    def __init__(self, master, canvas, width, height):
        self.master = master
        self.canvas = canvas
        self.img_width = width
        self.img_height = height

        self.logo_img = self.canvas.create_image(self.img_width / 2, self.img_height / 2)

        # self.canvas.tag_bind(self.editing_text,'<B1-Motion>', lambda e: self.move_text_anywhere_on_image(e.x, e.y))

        # move logo around image
        self.canvas.tag_bind(self.logo_img, '<B1-Motion>', lambda e: self.move_logo_any_where(e.x, e.y))
        # when image is clicked it brings back the logobox
        self.canvas.tag_bind(self.logo_img, '<Button-1>', lambda e: self.logo_box_clicked())
        # self.canvas.tag_bind(self.logo_img, '<Button-1>', lambda e: self.logo_box())

    def logo_box_clicked(self,*args):
        """gets executed if the logo_box was cliked by button 1"""
        self.logo_box_frame.destroy()
        # gets the scale before deleting the frame
        before_scale = round(self.float_var2.get(), 2)
        self.logo_box(scale=before_scale)

    def logo_box(self, *args, scale):
        style = Style()
        style.configure("custom.TFrame", background="white")
        self.logo_box_frame = ttk.Frame(self.master, height=600, width=400, )
        self.logo_box_frame.grid(row=1, column=0, sticky="NE", pady=15, padx=5)

        # Text box title
        self.logo_title_label = tk.Label(self.logo_box_frame, text="Properties",
                                         font=("New Times Roman", 15, "bold"), background="white", foreground="red")
        self.logo_title_label.grid(row=0, column=0, pady=7)
        # button to destroy the logobox frame
        with Image.open("./images/exit img.png").convert('RGBA') as img:
            resized_image = img.resize((15, 15), resample=3)

        self.delete_logoimg = ImageTk.PhotoImage(resized_image)
        self.logo_exit_button = ttk.Button(self.logo_box_frame, image=self.delete_logoimg,
                                           command=self.logo_box_frame.destroy)
        self.logo_exit_button.grid(row=0, column=1)

        self.float_var2 = tk.DoubleVar()
        if scale is None:
            self.float_var2.set(0.5)
        else:
            self.float_var2.set(scale)
        self.float_var2.trace('w', self.resize_logo)
        self.box_scale_label = tk.Label(self.logo_box_frame, text=f"Size: {self.float_var2.get()}x",
                                        foreground="#F0C38B", font=("New Times Roman", 10, "bold"))
        self.box_scale_label.grid(row=1, column=0, sticky="W")
        # # used to increase the size of the image
        img_size_scale_widget = ttk.Scale(self.logo_box_frame,
                                          from_=0.5,
                                          to=3.5,
                                          orient=tk.HORIZONTAL,
                                          variable=self.float_var2, length=200)

        img_size_scale_widget.grid(row=2, column=0, sticky="W", pady=20)

        # keeps track of the rotation of the image
        self.logo_int_var = tk.IntVar()
        self.logo_int_var.set(0)
        self.logo_int_var.trace('w', self.change_logo_rotation)

        self.logo_rotation_label = ttk.Label(self.logo_box_frame, text=f"Rotate: {self.logo_int_var.get()}")
        self.logo_rotation_label.grid(row=3, column=1, sticky="E", padx=10)

        # Scale widget for rotation of text
        rotation_scale_widget = ttk.Scale(self.logo_box_frame,
                                          from_=-180,
                                          to=180,
                                          orient=tk.HORIZONTAL,
                                          variable=self.logo_int_var, length=200)
        rotation_scale_widget.grid(row=3, column=0, sticky="W")

        # delete image made
        with Image.open("./images/trashcan-icon-5315275.jpg") as delete_image:
            resized_delete_image = delete_image.resize((20, 21), resample=3)
            self.delete_image = ImageTk.PhotoImage(resized_delete_image)

        delete_button = ttk.Button(self.logo_box_frame, image=self.delete_image, style="danger.TButton", command=lambda :self.delete_image_obj())
        delete_button.grid(row=4, column=1)
        delete_text = ttk.Label(self.logo_box_frame, text="delete")
        delete_text.grid(row=5, column=1, sticky="W")

    def resize_logo(self, master, *args):
        """Resizes the logo image"""

        width = int(self.initial_width * self.float_var2.get())
        height = int(self.initial_height * self.float_var2.get())
        # if the width is the same with the first resized width it reverts back to resizing without the resample paramter
        if width == (self.initial_width * 0.5):
            self.resized_logo = self.resized_logo.resize((width, height))
        else:
            self.resized_logo = self.resized_logo.resize((width, height), resample=Image.Resampling.LANCZOS)
        self.resize_image = ImageTk.PhotoImage(self.resized_logo)
        self.canvas.itemconfig(self.logo_img, image=self.resize_image)
        self.box_scale_label.configure(text=f"Size: {round(self.float_var2.get(), 2)}x")


    def move_logo_any_where(self, x, y):
        """moves the logo image around the image"""
        # makes sure the logo does not exceed the boundary of the image
        if y in range(0, self.img_height-20) and x in range(0, self.img_width-20):
            self.canvas.moveto(self.logo_img, x, y)

    def change_logo_rotation(self, *args):
        rotated_image = self.resized_logo.rotate(self.logo_int_var.get(), expand=True, fillcolor=(0, 0, 0, 0))
        self.resize_image = ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.logo_img, image=self.resize_image)
        self.logo_rotation_label.configure(text=f"Rotation: {self.logo_int_var.get()}")

    def delete_image_obj(self):
        """deletes the current image object"""
        self.logo_box_frame.destroy()
        self.canvas.delete(self.logo_img)

    def place_img(self, filename):
        """Places the image on the canvas"""
        if len(filename) != 0:
            with Image.open(filename).convert('RGBA') as self.logo:
                self.initial_width = 230
                self.initial_height = 300
                self.resized_logo = self.logo.resize((int(self.initial_width * 0.5), int(self.initial_height * 0.5)),
                                                     resample=3)
            self.new_logo = ImageTk.PhotoImage(self.resized_logo)
            self.canvas.itemconfig(self.logo_img, image=self.new_logo)

            self.logo_box(scale=None)













