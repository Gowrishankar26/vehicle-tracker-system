
import pymysql.cursors
import hashlib
from datetime import date




class DBConnection():
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="vechile_database",
            autocommit=True
        )
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


class Auth:
    def __init__(self,db):
        self.db=db
    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_admin(self):
        print("===Create Admin User Password===")
        username = input("Create admin Username: ")
        password = input("Create Password: ")
        hashed = self.hash_password(password)
        try:
            self.db.cursor.execute("INSERT INTO user(user_name, password_hash) VALUES (%s, %s)", (username, hashed))
            self.db.commit()
            print("Admin user created.")
        except:
            print("username already Exits")
    def login(self):
        print("====Login Required===")
        username=input("Username: ")
        password=input("Password: ")
        password_hash=self.hash_password(password)
        self.db.cursor.execute("select * from  user where user_name=%s and password_hash=%s ", ( username, password_hash))
        result=self.db.cursor.fetchone()
        if result:
            print(f"Welcome {username} !\n")
            return True
        else:
            print("Invalid Username or Password.\n")
            return False
class CustomerManager:
    def __init__(self,db):
        self.db=db
    def add_customer(self):
        print("===Add Customer===")
        name=input("Enter your name: ")
        phoneno=input("Enter your PhoneNo: ")
        emailid=input("Enter your EmailId: ")
        self.db.cursor.execute("insert into customer (name,phone,email) values(%s,%s,%s)",(name,phoneno,emailid))
        self.db.commit()
        print("Customer Added...")
    def see(self):
        self.db.cursor.execute("Select * from customer")
        rows = self.db.cursor.fetchall()
        if not rows:
            print("No customer record found.\n")
            return
        print("\n Customer list:")
        print("customer_id\t\tName\t\tPhone\t\tEmail")
        print("-" * 40)
        for row in rows:
            print(f"{row['costomer_id']}\t\t{row['name']:<10}\t\t{row['phone']:<10}\t\t{row['email']}")
class VechileManager:
    def __init__(self,db,customer_manager):
        self.db=db
        self.customer_manager=customer_manager

    def  add_vehicle(self):
        self.customer_manager.see()
        print("===Add Vechile===")
        customer_id=input("Enter Customer ID: ")
        model=input("Enter Model: ")
        regno=input("Enter Registration Number: ")
        try:
            self.db.cursor.execute("insert into vehicles(customer_id,model,registration_no) values(%s,%s,%s)",(customer_id,model,regno))
            self.db.commit()
            print("Vechile Added")
        except Exception as e:
            print(f"Error:{e}")

    def see1(self):
        self.db.cursor.execute("SELECT * FROM vehicles")
        rows = self.db.cursor.fetchall()
        if not rows:
            print("No vehicles record found.\n")
            return
        print("\n Vehicles list:")
        print("vehicles_id\t\t\tCustomer_id\t\t\tmodel\t\t\tregistration_no")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]}\t\t\t{row[1]:<10}\t\t\t{row[2]:<10}\t\t\t{row[3]}")


class ServiceManager:
    def __init__(self,db,vehicle_manger):
        self.db=db
        self.vehicle_manger=vehicle_manger
    def record_service(self):
        self.vehicle_manger.see1()
        print("===Record Service===")

        vechile_id=input("Enter Vechile Id: ")
        issue=input("Describe Service Issue: ")
        total_cost=float(input("How much total cost: "))
        service_date=date.today()
        self.db.cursor.execute("insert into services(vehicle_id,issues,total_cost,service_date) values(%s,%s,%s,%s)",
                                       (vechile_id,issue,total_cost,service_date))
        service_id=self.db.conn.insert_id()
        part_count=int(input("How many parts used: "))
        for _ in range(part_count):
            part_name = input("Enter the part used: ")
            part_cost = float(input("Enter the cost of part(₹): "))

            self.db.cursor.execute(
                "INSERT INTO part_used (services_id, part_name, part_cost) VALUES (%s, %s, %s)",
                (service_id, part_name, part_cost)
            )

        self.db.commit()
        print("Service Record Added sucessfully")

    def see2(self):
        self.db.cursor.execute("Select * from  services")
        rows = self.db.cursor.fetchall()
        if not rows:
            print("No service record found.\n")
            return
        print("\n Vehicles list:")
        print("service_id\t\t\tvehicle_id\t\t\tIssue\t\t\ttotal-cost\t\t\tservicedate")
        print("-" *60)
        for row in rows:
            print(f"{row['services_id']}\t\t\t{row['vehicle_id']:<10}\t\t\t{row['issues']:<10}\t\t\t{row['total_cost']}\t\t\t{row['service_date']}")

    def view_service_history(self):
        self.vehicle_manger.see1()
        print("==== View Service History ====")

        reg_no = input("Enter the Vehicle Registration Number: ")

        # Fetch service records for the given registration number
        self.db.cursor.execute("""
            SELECT s.services_id, s.service_date, s.issues, s.total_cost, v.model
            FROM services s
            JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            WHERE v.registration_no = %s
        """, (reg_no,))

        services = self.db.cursor.fetchall()

        if not services:
            print("No service record found for the vehicle.")
            return

        for service in services:
            service_id, service_date, issues, total_cost, model = service

            print(f"\nService ID: {service_id} | Model: {model} | Date: {service_date}")
            print(f"Issues: {issues}")
            print(f"Cost: ₹{float(total_cost):.2f}")
            print("   Parts Used:")

            # ✅ Fetch parts used for the current service
            self.db.cursor.execute("""
                SELECT part_name, part_cost FROM part_used
                WHERE services_id = %s
            """, (service_id,))
            parts = self.db.cursor.fetchall()

            if parts:
                for part_name, part_cost in parts:
                    print(f"   {part_name}: ₹{float(part_cost):.2f}")
            else:
                print("   No parts recorded.")


if __name__=="__main__":
    db=DBConnection()
    auth=Auth(db)
    cust_mgr=CustomerManager(db)
    veh_mgr=VechileManager(db,cust_mgr)
    ser_mgr=ServiceManager(db,veh_mgr)
    if auth.login():
        while True:
            print("\n===Vehicle Service Tracker====")
            print("1. Add Customer")
            print("2. Add Vehicle")
            print("3. Record Service")
            print("4. View Service History")
            print("5. Exit")
            choice = input("Choose the option(1-5): ")
            if choice == '1':
                cust_mgr.add_customer()
            elif choice == '2':
                veh_mgr.add_vehicle()
            elif choice == '3':
                 ser_mgr.record_service()
            elif choice == '4':
                ser_mgr.view_service_history()
            elif choice == '5':
                print("Thank you see you again.")
                break
            else:
                print("Invalid Choice. Try again.")
    else:
        print("Access Denied.")
    db.close()
