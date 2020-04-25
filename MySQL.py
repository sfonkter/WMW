import mysql.connector
import json
import os
import darkskyreq


class Database:
    def __init__(self, name):
        SQL_pass = os.environ['MYSQL_PASS']
        self._conn = mysql.connector.connect(host='localhost',
                                             database='users',
                                             user='wordpressuser',
                                             password=SQL_pass,
                                             )
        self._cursor = self._conn.cursor(buffered=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def byID(self, customer_id):
        sql = "SELECT * FROM information WHERE customer_id = '{}'"
        return self.query(sql.format(customer_id))

    def byPhone(self, phone):
        sql = "SELECT * FROM information WHERE phone = '{}'"
        return self.query(sql.format(phone))

    def usr(self, key, by=None):
        if by == None:
            row = self.byID(key)[0]
        elif by == 'byPhone':
            row = self.byPhone(key)[0]
        self.customer_id = row[0]
        self.first_name = row[1]
        self.last_name = row[2]
        self.phone = row[3]
        self.location = row[4]
        self.usr_time = row[5]
        self.gender = row[6]
        self.timezone = row[7]
        if self.first_name == '':
            return False
        return self

    def addUsr(self, pn='', n=None, info=''):
        column = {
            '0': 'first_name',
            '1': 'last_name',
            '2': 'gender',
            '3': 'location',
        }
        info.strip()
        try:
            customer_id = self.byPhone(pn)[0][0]
            if n == 3:
                w = darkskyreq.Weather(info)
                try:
                    address = w.getaddress()
                    tz = w.getweather().timezone
                    self.execute("UPDATE information SET location = '%s' WHERE customer_id = %s" % (info, customer_id))
                    self.execute("UPDATE information SET timezone = '%s' WHERE customer_id = %s" % (tz, customer_id))
                except Exception as e:
                    print(e)
                    return True
            elif n is not None:
                self.execute(
                    "UPDATE `information` SET %s = '%s' WHERE customer_id = %s" % (column[str(n)], info, customer_id))
        except Exception as e:
            print(e)
            self.execute("INSERT INTO `information` (phone) VALUES ('%s')" % (pn))

        self.commit()


def listed(x):
    with open('numbers.json', 'r') as f:
        nums = json.load(f)
    if x not in nums:
        nums.append(x)
        with open('numbers.json', 'w') as f:
            json.dump(nums, f, ensure_ascii=False, indent=4)
        return 1
