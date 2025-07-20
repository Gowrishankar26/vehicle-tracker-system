import pymysql.cursors
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="root"
)
cursor=conn.cursor()
cursor.execute("create database if not exists vechile_database")
print("Database created")
cursor.close()
conn.close()

