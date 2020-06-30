from tkinter import *
from tkinter import messagebox
from model.ticket import Ticket
from model.user import User
import view.ticket_result


class ConductorPanel:
    def __init__(self, session):
        self.root = None
        self.session = session
        self.entry = None

    def show(self):
        self.root = Tk()
        self.root.configure(background='#f0ffff')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (500, 200, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        form_frame = Frame(self.root, bg='#f0ffff')
        label = Label(form_frame, text='订单号：', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=0)
        self.entry = Entry(form_frame, bg='#FFFAFA', font=('微软雅黑', 10))
        self.entry.grid(row=0, column=1)
        form_frame.pack(fill=X, padx=120, pady=30)

        button_frame = Frame(self.root, bg='#f0ffff')
        button = Button(button_frame, text='查询', command=self.query, font=('微软雅黑', 12),
                        bg='#1e90ff', width=7)
        button.pack()
        button_frame.pack(fill=X, pady=30)

        self.root.mainloop()

    def query(self):
        ticket_id = self.entry.get()
        if ticket_id == '':
            messagebox.showerror('错误', '请输入订单号')
        else:
            ticket_info = self.session.query(Ticket.ticket_id, User.user_name, Ticket.train_id, Ticket.from_station_name, Ticket.to_station_name, Ticket.from_time, Ticket.to_time, Ticket.seat_type, Ticket.price, Ticket.date)\
                .join(User, User.user_id == Ticket.user_id).filter(Ticket.ticket_id == ticket_id).first()
            if ticket_info is None:
                messagebox.showerror('错误', '该订单号不存在')
            else:
                ticket_result = view.ticket_result.TicketResult(ticket_info, self.session)
                ticket_result.show()
