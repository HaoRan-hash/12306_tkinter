from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import and_
from sqlalchemy import func
from model.station import Station
from model.train_pass import TrainPass
from model.train_remain import TrainRemain
from model.train import Train
from model.ticket import Ticket
import view.id_result
import view.from_to_result
import view.user_center
from utils import find_train, handle_train_info
import datetime


class UserPanel:
    def __init__(self, session, user_id):
        self.session = session
        self.root = None
        self.combobox1 = None
        self.combobox2 = None
        self.combobox3 = None
        self.combobox4 = None
        self.combobox5 = None
        self.entry = None
        self.user_id = user_id

    def show(self):
        self.root = Tk()
        self.root.configure(background='#ffffe0')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (500, 320, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        root_frame1 = Frame(self.root, bg='#f0ffff')
        # 第一个frame
        form_frame1 = Frame(root_frame1, bg='#f0ffff')
        label1 = Label(form_frame1, text='出发地:', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=0)
        self.combobox1 = ttk.Combobox(form_frame1, width=10)
        self.combobox1.grid(row=0, column=1, padx=10)
        label2 = Label(form_frame1, text='目的地:', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=2)
        self.combobox2 = ttk.Combobox(form_frame1, width=10)
        self.combobox2.grid(row=0, column=3, padx=10)
        form_frame1.pack(fill=X, padx=75)

        # 第二个frame
        form_frame2 = Frame(root_frame1, bg='#f0ffff')
        label3 = Label(form_frame2, text='日期：', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=0)
        self.combobox3 = ttk.Combobox(form_frame2, width=7)
        self.combobox3.grid(row=0, column=1)
        label4 = Label(form_frame2, text='-', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=2)
        self.combobox4 = ttk.Combobox(form_frame2, width=7)
        self.combobox4.grid(row=0, column=3)
        label5 = Label(form_frame2, text='-', bg='#f0ffff', font=('微软雅黑', 12)).grid(row=0, column=4)
        self.combobox5 = ttk.Combobox(form_frame2, width=7)
        self.combobox5.grid(row=0, column=5)
        form_frame2.pack(fill=X, padx=95, pady=15)

        # 第三个frame
        button_frame1 = Frame(root_frame1, bg='#f0ffff')
        button1 = Button(button_frame1, text='查询', command=self.from_to_query, font=('微软雅黑', 12),
                         bg='#1e90ff', width=7)
        button1.grid(row=0, column=0, padx=200)
        button_frame1.pack(fill=X, padx=20, pady=5)
        root_frame1.pack(fill=X)

        root_frame2 = Frame(self.root, bg='#7fffd4')
        # 第四个frame
        form_frame3 = Frame(root_frame2, bg='#7fffd4')
        label6 = Label(form_frame3, text='车次：', bg='#7fffd4', font=('微软雅黑', 12)).grid(row=0, column=0)
        self.entry = Entry(form_frame3, bg='#FFFAFA', font=('微软雅黑', 10), width=17)
        self.entry.grid(row=0, column=1)
        form_frame3.pack(fill=X, padx=145, pady=15)

        # 第五个frame
        button_frame2 = Frame(root_frame2, bg='#7fffd4')
        button2 = Button(button_frame2, text='查询', command=self.id_query, font=('微软雅黑', 12),
                         bg='#00ff00', width=7)
        button2.grid(row=0, column=0, padx=200)
        button_frame2.pack(fill=X, padx=20, pady=5)
        root_frame2.pack(fill=X)

        root_frame3 = Frame(self.root, bg='#ffffe0')
        # 第六个frame
        button_frame3 = Frame(root_frame3, bg='#ffffe0')
        button3 = Button(button_frame3, text='个人中心', command=self.go_to_user_center, font=('微软雅黑', 12),
                         bg='#fffacd', width=7)
        button3.grid(row=0, column=0, padx=200)
        button_frame3.pack(fill=X, padx=20, pady=20)
        root_frame3.pack(fill=X)

        self.initialize()
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def initialize(self):
        station_names = self.session.query(Station.station_name).all()
        temp = []
        for i in range(len(station_names)):
            temp.append(station_names[i][0])
        temp = tuple(temp)
        self.combobox1['value'] = temp
        self.combobox2['value'] = temp

        self.combobox3['value'] = 2020
        self.combobox4['value'] = tuple(range(1, 13))
        self.combobox5['value'] = tuple(range(1, 32))

    def from_to_query(self):
        from_station_name = self.combobox1.get()
        to_station_name = self.combobox2.get()
        year = self.combobox3.get()
        month = self.combobox4.get()
        day = self.combobox5.get()
        if year == '' or month == '' or day == '':
            year = month = day = 1
        go_date = datetime.date(int(year), int(month), int(day))
        pass_from_station_train = self.session.query(TrainPass.train_id, Train.type, TrainPass.order, TrainPass.arrive_time, TrainPass.leave_time, TrainPass.mileage) \
            .join(Station, Station.station_id == TrainPass.station_id) \
            .join(Train, TrainPass.train_id == Train.train_id) \
            .filter(and_(TrainPass.is_stay == 1, Station.station_name == from_station_name)) \
            .all()
        pass_to_station_train = self.session.query(TrainPass.train_id, Train.type, TrainPass.order, TrainPass.arrive_time, TrainPass.leave_time, TrainPass.mileage) \
            .join(Station, Station.station_id == TrainPass.station_id) \
            .join(Train, TrainPass.train_id == Train.train_id) \
            .filter(and_(TrainPass.is_stay == 1, Station.station_name == to_station_name)) \
            .all()

        trains_info1, trains_info2 = find_train(pass_from_station_train, pass_to_station_train, from_station_name, to_station_name)

        for i in range(len(trains_info1)):
            temp = self.session.query(func.min(TrainRemain.seat_count), func.min(TrainRemain.bed_top_count)+func.min(TrainRemain.bed_mid_count)+func.min(TrainRemain.bed_bot_count)) \
                .filter(and_(TrainRemain.train_id == trains_info1[i][0], TrainRemain.order >= trains_info1[i][1], TrainRemain.order < trains_info1[i][2], TrainRemain.date == go_date)) \
                .all()

            trains_info2[i] = trains_info2[i] + temp[0]

        trains_info2.sort(key=lambda x: x[4])
        new_train_info = handle_train_info(trains_info2)

        from_to_result = view.from_to_result.FromToResult(new_train_info, self.session, go_date, self.user_id)
        from_to_result.show()

    def id_query(self):
        train_id = self.entry.get()
        if len(train_id) == 0:
            messagebox.showerror('错误', '车次不能为空')
        else:
            trains_info = self.session.query(TrainPass.order, Station.station_name, TrainPass.arrive_time, TrainPass.leave_time, TrainPass.is_stay) \
                .join(Station, Station.station_id == TrainPass.station_id) \
                .filter(TrainPass.train_id == train_id) \
                .all()
            trains_info.sort(key=lambda x: x[0])
            id_result = view.id_result.IdResult(trains_info)
            id_result.show()
            
    def go_to_user_center(self):
        user_ticket_info = self.session.query(Ticket.ticket_id, Ticket.train_id, Ticket.from_station_name, Ticket.to_station_name, Ticket.from_time, Ticket.to_time, Ticket.seat_type, Ticket.price, Ticket.date, Ticket.is_get)\
            .filter(Ticket.user_id == self.user_id).all()

        user_center = view.user_center.UserCenter(user_ticket_info)
        user_center.show()
