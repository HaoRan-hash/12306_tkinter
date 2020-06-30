from tkinter import *
from tkinter import messagebox
from sqlalchemy import and_
from model.user import User
import view.login_panel


class RegisterPanel:
    def __init__(self, session):
        self.session = session
        self.root = None
        self.entry1 = None
        self.entry2 = None
        self.entry3 = None
        self.role = None

    def show(self):
        self.root = Tk()
        self.root.configure(background='#f0ffff')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (500, 250, screen_width / 2, screen_height / 2))

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
        label3 = Label(form_frame, text='确认密码：', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=2, column=0)
        self.entry3 = Entry(form_frame, bg='#FFFAFA', font=('微软雅黑', 10), show='*')
        self.entry3.grid(row=2, column=1)
        form_frame.pack(fill=X, padx=120)

        # 第二个frame
        radio_frame = Frame(self.root, bg='#f0ffff')
        self.role = IntVar()
        self.role.set(0)
        rb1 = Radiobutton(radio_frame, text="用户", value=0, variable=self.role,
                          bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=0)
        rb2 = Radiobutton(radio_frame, text="售票员", value=1, variable=self.role,
                          bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=1, padx=20)
        radio_frame.pack(fill=X, padx=170, pady=20)

        # 第三个frame
        button_frame = Frame(self.root, bg='#f0ffff')
        button1 = Button(button_frame, text='确认注册', command=self.register, font=('微软雅黑', 12),
                         bg='#1e90ff', width=7)
        button1.grid(row=0, column=0)
        button_frame.pack(fill=X, padx=210)

        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def validate_register(self, user_name, password, confirm_password, role):
        if len(user_name) == 0 or user_name.isspace():
            messagebox.showerror('错误', '用户名不得为空')
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)
            self.entry3.delete(0, END)
            return False
        elif len(password) == 0 or password.isspace():
            messagebox.showerror('错误', '密码不得为空')
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)
            self.entry3.delete(0, END)
            return False
        elif confirm_password != password:
            messagebox.showerror('错误', '两次输入密码不一致')
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)
            self.entry3.delete(0, END)
            return False
        else:
            res = self.session.query(User) \
                .filter(and_(User.user_name == user_name, User.role == role)) \
                .all()
            if len(res) != 0:
                messagebox.showerror('错误', '该用户已被注册')
                self.entry1.delete(0, END)
                self.entry2.delete(0, END)
                self.entry3.delete(0, END)
                return False
            else:
                return True

    def register(self):
        user_name = self.entry1.get()
        password = self.entry2.get()
        confirm_password = self.entry3.get()
        role = self.role.get()
        if self.validate_register(user_name, password, confirm_password, role):
            new_user = User(user_name=user_name, password=password, role=role)
            self.session.add(new_user)
            self.session.commit()
            messagebox.showinfo('提示', '注册成功')
            self.close()
            login_panel = view.login_panel.LoginPanel(self.session)
            login_panel.show()
