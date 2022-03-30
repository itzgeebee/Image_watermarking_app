from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
from tkinter import filedialog
import matplotlib.pyplot as plt


class WaterMarkUI:
    def __init__(self):

        self.window = Tk()
        self.window.geometry("1000x800")
        self.window.title("Image watermarker")
        self.window.geometry()
        self.window.config(pady=50, padx=50)
        self.home_label = Label(text="Welcome, Please select an image to watermark")
        self.home_label.grid(row=0, column=1, padx=10, pady=10)

        self.get_image = Button(text="select Image", command=self.get_image)
        self.get_image.grid(row=1, column=1, padx=5, pady=5)

        self.edit_picture = Button(text="edit picture", command=self.edit_image)
        self.edit_picture.grid(row=3, column=1, padx=5, pady=5)

        self.save_changes = Button(text="save changes", command=self.save_image)
        self.save_changes.grid(row = 4, column=1, padx=5, pady=5 )

        self.watermark_img = Image.new('RGBA', (160, 160), (0, 0, 0, 0))

        self.window.mainloop()

    def edit_image(self):
        self.watermark_text_label = Label(text="Enter watermark")
        self.watermark_text_label.grid(row=0, column=2, padx=5, pady=5)
        self.watermark_text = Entry()
        self.watermark_text.grid(row=0, column=3, padx=5, pady=5)

        self.font_label = Label(text="Enter a font or use default")
        self.font_label.grid(row=1, column=2, padx=5, pady=5)
        self.font = Entry()
        self.font.grid(row=1, column=3, padx=5, pady=5)
        self.font.insert(0, "Arial")

        self.font_size_label = Label(text="enter font size")
        self.font_size_label.grid(row=2, column=2, padx=5, pady=5)
        self.fontsize = Entry()
        self.fontsize.grid(row=2, column=3, padx=20)

        self.position_label = Label(text="select text coordinates\n"
                                         "default coordinate: top-left")
        self.position_label.grid(row=3, column=2, padx=5, pady=5)
        self.position = Entry()
        self.position.grid(row=3, column=3, padx=5, pady=5)
        self.position.insert(0, "0,0")

        self.menu = StringVar()
        self.menu.set("Select a colour")
        self.color = OptionMenu(self.window, self.menu, "white", "black")
        self.color.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        self.transparency_label = Label(text="set transparency")
        self.transparency_label.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
        self.transparency = Scale(self.window, from_=0, to=255, orient=HORIZONTAL)
        self.transparency.grid(row=5, column=3, padx=5, pady=5)

        self.submit = Button(text="Submit changes", command=self.process_image)
        self.submit.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

    def get_image(self):
        global image
        self.window.file = filedialog.askopenfilename(
            filetypes=[('PNG Files', '*.PNG'), ("jpeg files", "*.jpg"), ("all files", "*.*")],
            initialdir="C:/Users/gb/Pictures", title="Select A file")
        self.img = Image.open(self.window.file)
        prev_img = self.img.resize((200, 200))
        image = ImageTk.PhotoImage(prev_img)
        image_label = Label(image=image, padx=5, pady=5).grid(row=2, column=1)

    def process_image(self):
        global new_image
        txt_position_1 = int(self.position.get().split(",")[0])
        txt_position_2 = int(self.position.get().split(",")[1])
        txt_position = (txt_position_1, txt_position_2)
        txt = self.watermark_text.get()
        font = ImageFont.truetype(f"{self.font.get().lower()}.ttf",
                                  size=int(self.fontsize.get()))

        transparency = self.transparency.get()
        if self.color == "white":
            fill = (255, 255, 255, transparency)
        else:
            fill = (0, 0, 0, transparency)
        self.img_copy = self.img.copy()

        ImageDraw.Draw(self.watermark_img).text(txt_position, txt, fill=fill, font=font)
        self.img_copy.paste(self.watermark_img, txt_position, self.watermark_img)
        prev_img_copy = self.img_copy.resize((400, 400))
        plt.imshow(self.img_copy)

        new_image = ImageTk.PhotoImage(prev_img_copy)

        print(new_image)
        new_image_label = Label(image=new_image, padx=5, pady=5).grid(row=2, column=1)

    def save_image(self):
        files = [('PNG Files', '*.PNG'),
                ("jpeg files", "*.jpg"),
                ("all files", "*.*")]

        watermarked_image = filedialog.asksaveasfile(filetypes=files,
                                            initialdir="C:/Users/gb/Pictures", title="Select A file", defaultextension=files[0][1])


