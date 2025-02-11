from ttkbootstrap import Style
from page import Frame


style = Style(theme="superhero")
root  = style.master
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.resizable(False, False)

# creating fixed geometry of the
# tkinter window with dimensions 150x200
root.geometry('900x600+300+100')
root.title("Image Watermark App")

window1 = Frame(root)


root.mainloop()