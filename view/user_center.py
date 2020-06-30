from tkinter import *
from tkinter import ttk


class UserCenter:
    def __init__(self, user_ticket_info):
        self.root = None
        self.user_ticket_info = user_ticket_info

    def show(self):
        self.root = Tk()
        self.root.configure(background='#ffffe0')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (700, 300, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        heads = ['订单号', '车次', '出发站', '到达站', '出发时间', '到达时间', '座位类型', '价格', '出发日期', '是否领取']
        tv = ttk.Treeview(self.root, columns=list(range(10)), show='headings')
        for i in range(10):
            tv.column(i, width=len(heads[i]) * 11, anchor='center')
            tv.heading(i, text=heads[i])

        self.handle_info()
        for i in self.user_ticket_info:
            tv.insert('', 'end', values=i)
        tv.pack(fill=BOTH)

        self.root.mainloop()

    def handle_info(self):
        for i in range(len(self.user_ticket_info)):
            temp = list(self.user_ticket_info[i])
            if temp[9] == 0:
                temp[9] = '否'
            else:
                temp[9] = '是'
            self.user_ticket_info[i] = tuple(temp)
