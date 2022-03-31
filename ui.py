# import tkinter and PIl
from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
from tkinter import filedialog, messagebox


class WaterMarkUI:
    def __init__(self):

        self.opener()

    def opener(self):
        """displays the first interface """
        # initialize tkinter GUI window
        self.window = Tk()
        self.window.geometry("1000x800")
        self.window.title("Image watermarker")
        self.window.config(pady=50, padx=200)

        # welcome message
        self.home_label = Label(text="Welcome, Please select an image to watermark")
        self.home_label.grid(row=0, column=1, padx=10, pady=10, )

        # select image button
        self.get_image = Button(text="select Image", command=self.get_image)
        self.get_image.grid(row=1, column=1, padx=5, pady=5, sticky="n")

        self.window.mainloop()

    def edit_image(self):
        """ a method for editing the selected image """

        # watermark text
        self.watermark_text_label = Label(text="Enter watermark")
        self.watermark_text_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.watermark_text = Entry()
        self.watermark_text.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # watermark font
        self.font_label = Label(text="Enter a font or use default")
        self.font_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.font = Entry()
        self.font.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.font.insert(0, "Arial")

        # font size
        self.font_size_label = Label(text="enter font size")
        self.font_size_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.fontsize = Entry()
        self.fontsize.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # watermark location
        self.position_label = Label(text="select text coordinates\n"
                                         "default coordinate: top-left")
        self.position_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.position = Entry()
        self.position.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.position.insert(0, "0,0")

        # watermark colour selector
        self.menu = StringVar()
        self.menu.set("Select a colour")
        self.color = OptionMenu(self.window, self.menu, "white", "black")
        self.color.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # set watermark transparency
        self.transparency_label = Label(text="set transparency")
        self.transparency_label.grid(row=9, column=0, padx=5, pady=5, sticky="e")
        self.transparency = Scale(self.window, from_=0, to=255, orient=HORIZONTAL)
        self.transparency.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # submit button calls the function to process the image
        self.submit = Button(text="Submit changes", command=self.process_image)
        self.submit.grid(row=10, column=1, padx=5, pady=5, )

    def get_image(self):

        self.window.file = filedialog.askopenfilename(
            filetypes=[('PNG Files', '*.PNG'), ("jpeg files", "*.jpg"), ("all files", "*.*")],
            initialdir="/", title="Select A file")
        self.display_image()

        self.edit_picture = Button(text="edit picture", command=self.edit_image)
        self.edit_picture.grid(row=3, column=1, padx=5, pady=5)

    def process_image(self):
        """This method gets all the user inputs, validates the inputs and either calls the display functions or returns an
         error message"""

        # validate text coordinate input
        try:
            txt_position_1 = int(self.position.get().split(",")[0])
        except ValueError:
            messagebox.showinfo(title="error", message=f"{self.position.get()} Invalid input. Please enter the "
                                                       f"coordinates "
                                                       f"in the format below:\n"
                                                       f"number,number e.g 0,0 or 20,20 or 100,100 depending on the "
                                                       f"image dimension\n "
                                                       f"do not add any empty spaces before, between or after numbers "
                                                       f"or comma")
        else:
            txt_position_2 = int(self.position.get().split(",")[1])
            self.txt_position = (txt_position_1, txt_position_2)
        txt = self.watermark_text.get()

        # validate font input from user
        try:
            self.wm_font = ImageFont.truetype(f"{self.font.get().lower()}.ttf",
                                              size=int(self.fontsize.get()))
        except OSError:
            messagebox.showinfo(title="error", message=f"{self.font.get()} font not found. Try another font")
        except ValueError:
            messagebox.showinfo(title="error",
                                message=f"{self.fontsize.get()} fontsize not found. Enter a valid number")

        # configure the text transparency
        transparency = self.transparency.get()
        if self.color == "white":
            self.fill = (255, 255, 255, transparency)
        else:
            self.fill = (0, 0, 0, transparency)
        self.img_copy = self.img.copy()

        # transparent watermark image
        self.watermark_img = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        self.attach_watermark(txt)

        # self.discard = Button(text="undo changes ❌", command=self.discard, bg="red")
        # self.discard.grid(row=3, column=2, padx=5, pady=5)

        # call the save image function
        self.save_changes = Button(text="save image ✅", command=self.save_image, bg="blue")
        self.save_changes.grid(row=3, column=0, padx=5, pady=5)

    def save_image(self):
        """ saves image to a specified directory in the specified format"""

        # define file save format
        files = [('PNG Files', '*.PNG'),
                 ("jpeg files", "*.jpg"),
                 ("all files", "*.*")]

        # open save location
        watermarked_image = filedialog.asksaveasfile(filetypes=files,
                                                     initialdir="/", title="Select A file",
                                                     defaultextension=files[0][1], mode="wb")
        if watermarked_image is None:
            return

        # save image
        self.img_copy.save(watermarked_image)
        watermarked_image.close()

        messagebox.showinfo(title="Saved image", message="Image saved successfully")

        # restart window
        self.window.destroy()
        self.opener()

    def display_image(self):
        """ displays the selected image on the tkinter window"""
        global image

        self.img = Image.open(self.window.file)
        self.width, self.height = self.img.size
        dimensions = self.adjust_dimensions()

        prev_img = self.img.resize((dimensions[0], dimensions[1]), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(prev_img)

        image_label = Label(text=f"image width = {self.width}, image height = {self.height})", image=image, padx=5,
                            pady=5)
        image_label.grid(row=2, column=1)

        messagebox.showinfo(title="image dimensions", message=f"These are the dimensions for the original image\n"
                                                              f"width: {self.width} height: {self.height}")

    # def discard(self):
    #     text = ""
    #     self.attach_watermark(text)

    def adjust_dimensions(self):
        """this method responsively adjusts image dimensions to fit the screen window
        for different image sizes"""

        new_width = 0
        new_height = 0
        if self.width > 1000:
            new_width = self.width // 3
            new_height = self.height // 3
        elif self.width < 400:
            new_width = self.width
            new_height = self.height
        else:
            new_width = self.width // 2
            new_height = self.height // 2
        return [new_width, new_height]

    def attach_watermark(self, txt):
        """places the transparent watermark image and text on top of the copied image"""
        global new_image

        ImageDraw.Draw(self.watermark_img).text(self.txt_position, txt, fill=self.fill, font=self.wm_font)
        self.img_copy.paste(self.watermark_img, self.txt_position, self.watermark_img)
        dimensions = self.adjust_dimensions()
        prev_img_copy = self.img_copy.resize((dimensions[0], dimensions[1]), Image.ANTIALIAS)

        new_image = ImageTk.PhotoImage(prev_img_copy)
        new_image_label = Label(image=new_image, padx=5, pady=5).grid(row=2, column=1)
