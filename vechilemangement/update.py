# import hashlib
# import pymysql
#
# conn = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="vechile_database"
# )
# cursor = conn.cursor()
#
# username = "gowri"  # your admin username
# new_password = "password"  # your new password
# hashed = hashlib.sha256(new_password.encode()).hexdigest()
#
# # Update password
# cursor.execute("UPDATE user SET  user_name=%s where password_hash=%s ", (hashed, username))
# conn.commit()
# print("Password reset successful.")
#
# cursor.close()
# conn.close()

import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="vechile_database"
)
cursor = conn.cursor()

old_username = "1234"       # 🔁 Replace with the old one
new_username = "gowri shankar"   # 🔁 Replace with your new desired username

try:
    #cursor.execute("UPDATE user SET user_name=%s WHERE user_name=%s", (new_username, old_username))
    cursor.execute("alter table services add service_date date")
    print("Username updated successfully.")
except Exception as e:
    print("Failed to update username:", e)

cursor.close()
conn.close()

