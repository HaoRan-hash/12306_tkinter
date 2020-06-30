from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import func
from model.ticket import Ticket
from model.train_pass import TrainPass
from model.station import Station
from model.train_remain import TrainRemain
import random
import datetime


class FromToResult:
    def __init__(self, trains_info, session, go_date, user_id):
        self.root = None
        self.session = session
        self.combobox = None
        self.tv = None
        self.trains_info = trains_info
        self.go_date = go_date
        self.user_id = user_id

    def show(self):
        self.root = Tk()
        self.root.configure(background='#f0ffff')
        # 使窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" % (600, 300, screen_width / 2, screen_height / 2))

        # 设置窗口不可调整
        self.root.resizable(width=False, height=False)

        heads = ['车次', '出发站', '到达站', '出发时间', '到达时间', '硬座', '卧铺', '硬座价格', '卧铺价格']
        self.tv = ttk.Treeview(self.root, columns=list(range(9)), show='headings')
        for i in range(9):
            self.tv.column(i, width=len(heads[i]) * 11, anchor='center')
            self.tv.heading(i, text=heads[i])

        self.handle_info()
        for i in self.trains_info:
            self.tv.insert('', 'end', values=i)
        self.tv.pack(fill=BOTH)

        button = Button(self.root, text='购买', command=self.purchase, font=('微软雅黑', 12),
                        bg='#1e90ff', width=7)
        button.pack(side=RIGHT, padx=10)
        self.combobox = ttk.Combobox(self.root, width=15)
        self.combobox['value'] = ('硬座', '卧铺')
        self.combobox.pack(side=RIGHT, padx=20)
        self.root.mainloop()

    def handle_info(self):
        for i in range(len(self.trains_info)):
            if self.trains_info[i][5] == 0 or self.trains_info[i][6] is None:
                self.trains_info[i][5] = '无'
            else:
                self.trains_info[i][5] = '有'

            if self.trains_info[i][6] == 0 or self.trains_info[i][6] is None:
                self.trains_info[i][6] = '无'
            else:
                self.trains_info[i][6] = '有'

    @staticmethod
    def validate_purchase(choose_train, choose_seat):
        if len(choose_train) == 0:
            messagebox.showerror('错误', '当前未选择车次')
            return False
        elif choose_seat == '':
            messagebox.showerror('错误', '当前未选择座位类型')
            return False
        else:
            return True

    @staticmethod
    def random_selection(bed_count):
        temp = []
        if bed_count[0] != 0:
            temp.append('上铺')
        if bed_count[1] != 0:
            temp.append('中铺')
        if bed_count[2] != 0:
            temp.append('下铺')
        bed_type = random.randint(0, len(temp)-1)
        return temp[bed_type]

    @staticmethod
    def split_time(choose_train):
        res1 = choose_train[3].split(':')
        res2 = choose_train[4].split(':')
        for i in range(3):
            res1[i] = int(res1[i])
        for i in range(3):
            res2[i] = int(res2[i])
        return res1, res2

    def purchase(self):
        choose_train = self.tv.selection()
        choose_seat = self.combobox.get()
        if self.validate_purchase(choose_train, choose_seat):
            choose_train = self.tv.item(self.tv.selection()[0], 'values')
            split_from_time, split_to_time = self.split_time(choose_train)
            from_time = datetime.time(split_from_time[0], split_from_time[1], split_from_time[2])
            to_time = datetime.time(split_to_time[0], split_to_time[1], split_to_time[2])

            # 第一步，检查之前是否购买过当天的该车次
            is_purchase = self.session.query(Ticket).filter(Ticket.user_id == self.user_id, Ticket.train_id == choose_train[0], Ticket.date == self.go_date).count()
            if is_purchase != 0:
                messagebox.showerror('错误', '您已经购买过当天的该车次，不能重复购买')
            else:
                # 第二步，检查当前该车次是否还有余票，因为别的用户也在操作，列表中的信息已经滞后了
                from_order = self.session.query(TrainPass.order)\
                    .join(Station, Station.station_id == TrainPass.station_id)\
                    .filter(TrainPass.train_id == choose_train[0], Station.station_name == choose_train[1]).first()
                to_order = self.session.query(TrainPass.order) \
                    .join(Station, Station.station_id == TrainPass.station_id) \
                    .filter(TrainPass.train_id == choose_train[0], Station.station_name == choose_train[2]).first()

                if choose_seat == '硬座':
                    seat_count = self.session.query(func.min(TrainRemain.seat_count))\
                        .filter(TrainRemain.train_id == choose_train[0], TrainRemain.order >= from_order[0], TrainRemain.order < to_order[0])\
                        .all()

                    if seat_count[0][0] == 0:
                        messagebox.showerror('错误', '票已售完')
                    else:
                        # 更新区间余票信息(都减1)
                        self.session.query(TrainRemain)\
                            .filter(TrainRemain.train_id == choose_train[0], TrainRemain.order >= from_order[0], TrainRemain.order < to_order[0])\
                            .update({TrainRemain.seat_count: TrainRemain.seat_count-1}, synchronize_session="evaluate")

                        # 生成订单
                        new_ticket = Ticket(user_id=self.user_id, train_id=choose_train[0], from_station_name=choose_train[1],
                                            to_station_name=choose_train[2], from_time=from_time, to_time=to_time, seat_type=choose_seat, price=int(choose_train[7]), date=self.go_date, is_get=0)
                        self.session.add(new_ticket)
                        self.session.commit()

                        messagebox.showinfo('提示', '购买成功')

                else:
                    bed_count = self.session.query(func.min(TrainRemain.bed_top_count), func.min(TrainRemain.bed_mid_count), func.min(TrainRemain.bed_bot_count)) \
                        .filter(TrainRemain.train_id == choose_train[0], TrainRemain.order >= from_order[0], TrainRemain.order < to_order[0]) \
                        .all()

                    if bed_count[0][0] + bed_count[0][1] + bed_count[0][2] == 0:
                        messagebox.showerror('错误', '票已售完')
                    else:
                        bed_type = self.random_selection(bed_count[0])

                        if bed_type == '上铺':
                            # 更新区间余票信息(都减1)
                            self.session.query(TrainRemain) \
                                .filter(TrainRemain.train_id == choose_train[0], TrainRemain.order >= from_order[0], TrainRemain.order < to_order[0]) \
                                .update({TrainRemain.bed_top_count: TrainRemain.bed_top_count - 1}, synchronize_session="evaluate")

                            # 生成订单
                            new_ticket = Ticket(user_id=self.user_id, train_id=choose_train[0], from_station_name=choose_train[1],
                                                to_station_name=choose_train[2], from_time=from_time, to_time=to_time, seat_type='上铺', price=int(choose_train[8]), date=self.go_date, is_get=0)
                            self.session.add(new_ticket)
                            self.session.commit()

                            messagebox.showinfo('提示', '购买成功(上铺)')
                        elif bed_type == '中铺':
                            # 更新区间余票信息(都减1)
                            self.session.query(TrainRemain) \
                                .filter(TrainRemain.train_id == choose_train[0], TrainRemain.order >= from_order[0], TrainRemain.order < to_order[0]) \
                                .update({TrainRemain.bed_mid_count: TrainRemain.bed_mid_count - 1}, synchronize_session="evaluate")

                            # 生成订单
                            new_ticket = Ticket(user_id=self.user_id, train_id=choose_train[0], from_station_name=choose_train[1],
                                                to_station_name=choose_train[2], from_time=from_time, to_time=to_time, seat_type='中铺', price=int(int(choose_train[8])*1.03), date=self.go_date, is_get=0)
                            self.session.add(new_ticket)
                            self.session.commit()

                            messagebox.showinfo('提示', '购买成功(中铺)')
                        else:
                            # 更新区间余票信息(都减1)
                            self.session.query(TrainRemain) \
                                .filter(TrainRemain.train_id == choose_train[0], TrainRemain.order >= from_order[0], TrainRemain.order < to_order[0]) \
                                .update({TrainRemain.bed_bot_count: TrainRemain.bed_bot_count - 1}, synchronize_session="evaluate")

                            # 生成订单
                            new_ticket = Ticket(user_id=self.user_id, train_id=choose_train[0], from_station_name=choose_train[1],
                                                to_station_name=choose_train[2], from_time=from_time, to_time=to_time, seat_type='下铺', price=int(int(choose_train[8]) * 1.07), date=self.go_date, is_get=0)
                            self.session.add(new_ticket)
                            self.session.commit()

                            messagebox.showinfo('提示', '购买成功(下铺)')
