from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from model.ticket import Ticket


class TicketResult:
    def __init__(self, ticket_info, session):
        self.root = None
        self.ticket_info = ticket_info
        self.session = session

    def show(self):
        self.root = Tk()
        self.root.configure(background='#f0ffff')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (700, 300, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        heads = ['订单号', '用户名', '车次', '出发站', '到达站', '出发时间', '到达时间', '座位类型', '价格', '出发日期']
        tv = ttk.Treeview(self.root, columns=list(range(10)), show='headings')
        for i in range(10):
            tv.column(i, width=len(heads[i]) * 11, anchor='center')
            tv.heading(i, text=heads[i])

        tv.insert('', 'end', values=self.ticket_info)
        tv.pack(fill=BOTH)

        button = Button(self.root, text='取票', command=self.get_ticket, font=('微软雅黑', 12),
                        bg='#1e90ff', width=7)
        button.pack(side=RIGHT, padx=10)

        self.root.mainloop()

    def get_ticket(self):
        is_get = self.session.query(Ticket.is_get).filter(Ticket.ticket_id == self.ticket_info[0]).first()

        if is_get[0] == 0:
            self.session.query(Ticket).filter(Ticket.ticket_id == self.ticket_info[0])\
                .update({Ticket.is_get: Ticket.is_get+1}, synchronize_session="evaluate")
            self.session.commit()
            messagebox.showinfo('提示', '领取成功')
        else:
            messagebox.showerror('错误', '你已领取该车票')
