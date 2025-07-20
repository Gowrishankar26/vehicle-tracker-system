import pymysql.cursors
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="vechile_database"
)
cursor=conn.cursor()
cursor.execute("""create table if not exists user(user_id  int auto_increment primary key,user_name varchar(30) unique,password_hash varchar(20))""")
cursor.execute("""create table if not exists customer(costomer_id  int auto_increment primary key,name varchar(30) ,phone varchar(10),email varchar(30))""")
cursor.execute("""create table if not exists vehicles(vehicle_id  int auto_increment primary key,customer_id int,model varchar(10),registration_no varchar(20) unique,
foreign key(customer_id) references customer(costomer_id))""")
cursor.execute("""create table if not exists services(services_id  int auto_increment primary key,vehicle_id int,issues text,total_cost decimal(10,2),
foreign key(vehicle_id) references vehicles(vehicle_id))""")
cursor.execute("""create table if not exists part_used(part_id  int auto_increment primary key,services_id int,part_name varchar(10),part_cost decimal(10,2),
foreign key(services_id) references services(services_id))""")
cursor.close()
conn.close()