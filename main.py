import csv
import pickle
from tabulate import tabulate

product_details = {}
purchase_details = {}
sales_details = {}

product_details_file = 'product_details.pkl'
purchase_details_file = 'purchase_details.pkl'
sales_details_file = 'sales_details.pkl'

def save_data():
    with open(product_details_file, 'wb') as f:
        pickle.dump(product_details, f)
    with open(purchase_details_file, 'wb') as f:
        pickle.dump(purchase_details, f)
    with open(sales_details_file, 'wb') as f:
        pickle.dump(sales_details, f)
    print("Data saved successfully.")

def load_data():
    global product_details, purchase_details, sales_details
    try:
        with open(product_details_file, 'rb') as f:
            product_details = pickle.load(f)
        with open(purchase_details_file, 'rb') as f:
            purchase_details = pickle.load(f)
        with open(sales_details_file, 'rb') as f:
            sales_details = pickle.load(f)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No existing data found. Starting with empty dictionaries.")


load_data()

def signup():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Check if the username already exists
    if username in users:
        print("Username already exists. Please try again.")
    else:
        users[username] = password
        save_users()
        print("Signup successful. Please login.")

def load_users():
    try:
        with open('users.csv', 'r') as f:
            reader = csv.reader(f)
            
            for row in reader:
                if len(row) >= 2:
                    username = row[0]
                    password = row[1]
                    users[username] = password
    except FileNotFoundError:
        return
                
users = {}  # Dictionary to store user credentials
def save_users():
    print("Save users function was called")
    with open('users.csv', 'w') as f:
        writer = csv.writer(f)
        for username, password in users.items():
            writer.writerow([username, password])



# Load existing users from file
load_users()
      
def store_purchase_details():
    
    print("__Purchase Details__")
    product_id = input("Enter product ID: ")
    supplier_name = input("Enter supplier name: ")
    supplier_address = input("Enter supplier address: ")
    purchase_date = input("Enter purchase date: ")
    wholesale_rate = float(input("Enter wholesale rate: "))
    units_bought = int(input("Enter number of units bought: "))

    details = [supplier_name, supplier_address, purchase_date, wholesale_rate, units_bought]
    purchase_details[product_id] = details
    store_sales_details(product_id)

def store_sales_details(id):
    cmd = input("Do you want to enter sales details for this prodict (Y/N): ")
    if cmd in "YyyesYesYeahyeahokayOkayOKokOk":
        print("__Sales Details__")
        product_id = id
        sales_date = input("Enter sales date: ")
        units_sold = int(input("Enter number of units sold: "))
        retail_price = float(input("Enter retail price: "))

        details = [sales_date, units_sold, retail_price]
        sales_details[product_id] = details
def Report():
    print()
    print("Purchase Details")
    pdheader = ["ID","Supplier", "Supplier Address", "Date of Purchase", "Wholesale Rate", "Units Bought"]
    pd = []
    pd.append(pdheader)
    for i in purchase_details:
        pdsub = []
        pdsub.append(i)
        pdsub.append(purchase_details[i][0])
        pdsub.append(purchase_details[i][1])
        pdsub.append(purchase_details[i][2])
        pdsub.append(purchase_details[i][3])
        pdsub.append(purchase_details[i][4])
        pd.append(pdsub)
    print(tabulate(pd))
    
    print("\nSales Details")
    sdheader = ["ID","Sales Date", "Units Sold", "Retail Price"]
    sd = []
    sd.append(sdheader)
    for i in sales_details:
        sdsub = []
        sdsub.append(i)
        sdsub.append(sales_details[i][0])
        sdsub.append(sales_details[i][1])
        sdsub.append(sales_details[i][2])
      
        sd.append(sdsub)
    print(tabulate(sd))

    #print("Product Details in The Format - Supplier Name, Stock Count, Units Sold, MRP, Profit/Loss (If negative, its a loss)")
    print("\nProduct Details")
    prdheader = ["ID","Current Stock", "Stock Sold", "Supplier", "MRP",  "Profit/Loss"]
    prd = []
    prd.append(prdheader)
    for i in product_details:
        prdsub = []
        prdsub.append(i)
        prdsub.append(product_details[i][0])
        prdsub.append(product_details[i][3])
        prdsub.append(product_details[i][2])
        prdsub.append(product_details[i][1])
        prdsub.append(product_details[i][4])
        
        prd.append(prdsub)
        
    print(tabulate(prd))
    
def create_product_details():

    for product_id in purchase_details:
        if product_id in sales_details:
            purchase_info = purchase_details[product_id]
            sales_info = sales_details[product_id]

            stock_count = purchase_info[4] - sales_info[1]
            mrp = sales_info[2]
            supplier_name = purchase_info[0]
            units_sold = sales_info[1]
            profit =  mrp * units_sold - purchase_info[3]* purchase_info[4] 

            product_details[product_id] = [stock_count, mrp, supplier_name, units_sold, profit]
        else:
            purchase_info = purchase_details[product_id]

            stock_count = purchase_info[4] - 0
            mrp = sales_info[2]
            supplier_name = purchase_info[0]
            units_sold = 0


            product_details[product_id] = [stock_count, mrp, supplier_name, units_sold, "No profit was generated"]
def rolecheck():
    role = int(input("What's Your Role? 1: Owner, 2: Manager  ::  "))
    while True:
        if (role == 1):
            cmd = int(input("1 : Add Details \n2: Modify Details\n3: Delete Details\n4: Report\n"))
            if cmd == 1:
                n = int(input("Enter the number of products : "))
                for i in range(n):
                    print ("Product ", i+1)
                    store_purchase_details()
                    print("*" * 20)
                create_product_details()
                save_data()
                input("\nPress Enter To Perform Tasks...")
            elif cmd == 2 :
                product_id = input("Enter Product ID : ")
                supplier_name = input("Enter supplier name: ")
                supplier_address = input("Enter supplier address: ")
                purchase_date = input("Enter purchase date: ")
                wholesale_rate = float(input("Enter wholesale rate: "))
                units_bought = int(input("Enter number of units bought: "))

                details = [supplier_name, supplier_address, purchase_date, wholesale_rate, units_bought]
                purchase_details[product_id] = details
                store_sales_details(product_id)
                save_data()
                input("\nPress Enter To Perform Tasks...")
            elif cmd == 3 :
                product_id = input("Enter Product ID : ")
                del purchase_details[product_id]
                if(product_id in sales_details):
                    del sales_details[product_id]
                del product_details[product_id]
                
                save_data()
                input("\nPress Enter To Perform Tasks...")
            elif cmd == 4:
                Report()
                input("\nPress Enter To Perform Tasks...")
                
                
        elif (role == 2):
            cmd = int(input("1 : Modify Details\n2 : Report\n"))
            if cmd == 1 :
                product_id = input("Enter Product ID : ")
                supplier_name = input("Enter supplier name: ")
                supplier_address = input("Enter supplier address: ")
                purchase_date = input("Enter purchase date: ")
                wholesale_rate = float(input("Enter wholesale rate: "))
                units_bought = int(input("Enter number of units bought: "))

                details = [supplier_name, supplier_address, purchase_date, wholesale_rate, units_bought]
                purchase_details[product_id] = details
                store_sales_details(product_id)
                save_data()
                input("\nPress Enter To Perform Tasks...")
            
            elif cmd == 2:
                Report()
                input("\nPress Enter To Perform Tasks...")
            

while True:
    print("1. Login")
    print("2. Signup")
    print("3. Quit")

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in users and users[username] == password:
            print("Login successful.")
            rolecheck()
            break
        else:
            print("Invalid username or password.")
    elif choice == "2":
        signup()
    elif choice == "3":
            
        print("Program exited.")
        break
    else:
        print("Invalid choice. Please try again.")
