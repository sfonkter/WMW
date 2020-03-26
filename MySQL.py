import mysql.connector
import userlist

mydb = mysql.connector.connect(user = 'doadmin', password = 'poamfy2bog7z5iq2',
    host = 'wmwuserinfo-do-user-7206460-0.a.db.ondigitalocean.com',
    port = 25060,
    db = 'users'
)

cursor = mydb.cursor()

add_user = ("INSERT INTO information "
"(customer_id, first_name, last_name, phone, location, time, gender, timezone) "
"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

for x in range (0, len(userlist.read())):
    usr = userlist.loadUser(userlist.read()[x]['phone'])
    print(x)
    print(usr.first)
    data_usr = (x+1, usr.first, usr.last, usr.phone, usr.location, usr.time, usr.gender, usr.timezone)

    cursor.execute(add_user, data_usr)
    emp_no = cursor.lastrowid

mydb.commit()
cursor.close()
mydb.close()
