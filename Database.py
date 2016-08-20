import pymysql.cursors
import config


class Database:
    def __init__(self):
        self.conn = pymysql.connect(host=config.host,
                                    user=config.user,
                                    password=config.password,
                                    db=config.db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
