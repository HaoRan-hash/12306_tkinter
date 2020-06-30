from tkinter import *
from tkinter import messagebox
from sqlalchemy import and_
from model.user import User
import view.user_panel
import view.register_panel
import view.conductor_panel


class LoginPanel:
    def __init__(self, session):
        self.session = session
        self.root = None
        self.entry1 = None
        self.entry2 = None
        self.role = None  # 默认为用户

    def show(self):
        self.root = Tk()
        self.root.configure(background='#f0ffff')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (500, 200, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        # 第一个frame
        form_frame = Frame(self.root, bg='#f0ffff')
        label1 = Label(form_frame, text='用户名：', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=0)
        self.entry1 = Entry(form_frame, bg='#FFFAFA', font=('微软雅黑', 10))
        self.entry1.grid(row=0, column=1)
        label2 = Label(form_frame, text='密码：', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=1, column=0)
        self.entry2 = Entry(form_frame, bg='#FFFAFA', font=('微软雅黑', 10), show='*')
        self.entry2.grid(row=1, column=1, pady=15)
        form_frame.pack(fill=X, padx=120)

        # 第二个frame
        radio_frame = Frame(self.root, bg='#f0ffff')
        self.role = IntVar()
        self.role.set(0)
        rb1 = Radiobutton(radio_frame, text="用户", value=0, variable=self.role,
                          bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=0)
        rb2 = Radiobutton(radio_frame, text="售票员", value=1, variable=self.role,
                          bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=1, padx=20)
        radio_frame.pack(fill=X, padx=170, pady=10)

        # 第三个frame
        button_frame = Frame(self.root, bg='#f0ffff')
        button1 = Button(button_frame, text='登录', command=self.login, font=('微软雅黑', 12),
                         bg='#1e90ff', width=7)
        button1.grid(row=0, column=0)
        button2 = Button(button_frame, text='注册', command=self.go_register, font=('微软雅黑', 12),
                         bg='#1e90ff', width=7)
        button2.grid(row=0, column=1, padx=80)
        button_frame.pack(fill=X, padx=120)

        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def validate_login(self, user_name, password, role):
        if len(user_name) == 0 or user_name.isspace():
            messagebox.showerror('错误', '用户名不得为空')
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)
            return False
        elif len(password) == 0 or password.isspace():
            messagebox.showerror('错误', '密码不得为空')
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)
            return False
        else:
            res = self.session.query(User)\
                .filter(and_(User.user_name == user_name, User.password == password, User.role == role))\
                .all()
            if len(res) == 0:
                messagebox.showerror('错误', '用户名或密码错误')
                self.entry1.delete(0, END)
                self.entry2.delete(0, END)
                return False
            else:
                return True

    def login(self):
        user_name = self.entry1.get()
        password = self.entry2.get()
        role = self.role.get()
        if self.validate_login(user_name, password, role):
            messagebox.showinfo('提示', '登录成功')
            user_id = self.session.query(User.user_id).filter(User.user_name == user_name, User.role == role).first()
            self.close()
            if role == 0:
                user_panel = view.user_panel.UserPanel(self.session, user_id[0])
                user_panel.show()
            else:
                conductor_panel = view.conductor_panel.ConductorPanel(self.session)
                conductor_panel.show()

    def go_register(self):
        self.close()
        register_panel = view.register_panel.RegisterPanel(self.session)
        register_panel.show()
