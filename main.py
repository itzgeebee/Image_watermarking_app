from ui import WaterMarkUI


page = WaterMarkUI()

















# def get_files():
#     global image
#     window.file = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg'), ("all files", "*.*")], initialdir="C:/Users/gb/Pictures", title = "Select A file")
#     my_label = Label(window, text=window.file)
#     # my_label.pack()
#     # image = ImageTk.PhotoImage(Image.open(window.file))
#     # image_label = Label(image=image).pack()
#     # print(my_label)
#
#     return window.file
#
#
#
#
#
#
#
#
# def watermark_with_transparency(input_image_path,
#                                 output_image_path,
#                                 watermark_image_path,
#                                 position):
#     base_image = Image.open(input_image_path)
#     watermark = Image.open(watermark_image_path)
#     width, height = base_image.size
#     transparent = Image.new('RGBA', (width, height), (0,0,0,0))
#     transparent.paste(base_image, (0,0))
#     transparent.paste(watermark, position, mask=watermark)
#     transparent.show()
#     transparent.save(output_image_path)



# window.mainloop()