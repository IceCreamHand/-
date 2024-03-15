import tkinter as tk
from tkinter import Canvas, Label, Scrollbar, Menu, filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("脑部扫描图像查看器")
        self.geometry("1200x800")

        # 创建菜单栏
        menubar = Menu(self)

        # 创建文件菜单
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="打开图像", command=self.load_image)
        menubar.add_cascade(label="文件", menu=file_menu)
        menubar.add_cascade(label="标注", menu=file_menu)
        menubar.add_cascade(label="撤销", menu=file_menu)
        menubar.add_cascade(label="分析", menu=file_menu)
        menubar.add_cascade(label="设置", menu=file_menu)
        menubar.add_cascade(label="帮助", menu=file_menu)

        # 创建缩放菜单
        zoom_menu = Menu(menubar, tearoff=0)
        zoom_menu.add_command(label="放大", command=self.zoom_in)
        zoom_menu.add_command(label="缩小", command=self.zoom_out)
        menubar.add_cascade(label="缩放", menu=zoom_menu)


        # 设置菜单栏
        self.config(menu=menubar)

        # 创建画布，用于显示图像
        self.canvas = Canvas(self, bg="black", width=1200, height=350)
        self.canvas.pack(padx=10, pady=10)
        self.canvas = Canvas(self, bg="black", width=1200, height=350)
        self.canvas.pack(padx=10, pady=10)

        # 初始化变量
        self.current_image = None
        self.scale_factor = 1.0

        # 创建标签，用于显示测量数据
        self.measurement_label = Label(self, text="对照结果：x", font=("Arial", 12))
        self.measurement_label.pack(pady=10)

        # 创建滚动条
        self.scrollbar = Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 将滚动条与画布关联
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            image = Image.open(file_path)
            self.scale_factor = 1.0
            self.resize_image(image)

    def zoom_in(self):
        self.scale_factor *= 1.25
        self.resize_image()

    def zoom_out(self):
        if self.scale_factor > 0.25:
            self.scale_factor /= 1.25
            self.resize_image()

    def resize_image(self, image):
        if image:
            new_width = int(image.width * self.scale_factor)
            new_height = int(image.height * self.scale_factor)
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
            self.current_image = photo

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()