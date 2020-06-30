from tkinter import *
from tkinter import ttk


class IdResult:
    def __init__(self, trains_info):
        self.trains_info = trains_info
        self.root = None

    def show(self):
        self.root = Tk()
        self.root.configure(background='#7fffd4')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (500, 300, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        heads = ['站序', '站名', '到时', '发时', '是否停留']
        tv = ttk.Treeview(self.root, columns=list(range(5)), show='headings')
        for i in range(5):
            tv.column(i, width=len(heads[i]) * 11, anchor='center')
            tv.heading(i, text=heads[i])
        self.handle_info()
        for i in self.trains_info:
            tv.insert('', 'end', values=i)
        tv.pack(fill=BOTH)

        self.root.mainloop()

    def handle_info(self):
        for i in range(len(self.trains_info)):
            temp = list(self.trains_info[i])
            if temp[2] is None:
                temp[2] = '----'
            if temp[3] is None:
                temp[3] = '----'

            if temp[4] == 0:
                temp[4] = '否'
            else:
                temp[4] = '是'
            self.trains_info[i] = tuple(temp)
