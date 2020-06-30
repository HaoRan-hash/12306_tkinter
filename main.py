from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from view.login_panel import LoginPanel

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/train_12306?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    login_panel = LoginPanel(session)
    login_panel.show()
