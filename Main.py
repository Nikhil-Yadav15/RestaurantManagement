import mysql.connector
from tabulate import tabulate
import sys
import datetime as DT
import fontstyle
import maskpass

class Manage():
    def __init__(self):
        self.db = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '*********', database = '#######')
        self.mycursor = self.db.cursor(buffered=True)
        
    def begin(self, d=0):
        if d == 1:
            print('\t\t\t', fontstyle.apply('\n\t\t\tRestaurant Management System', 'bold/Italic/blue'))
        
        print(fontstyle.apply('\nYou are:\n1. Customer\n2. Owner\n3. Exit', 'Italic/darkcyan'))
        
        self.ask = int(input(fontstyle.apply('\nEnter your choice: ', 'Italic/purple')))
        if self.ask == 1:
            self.cust()
        elif self.ask == 2:
            self.owner()
        elif self.ask == 3:
            print(fontstyle.apply('\n\t\tThankYou!', 'Italic/blue'))
            sys.exit()
        else:
            print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
            self.begin()
    def cust(self):
        print(fontstyle.apply('\nDo you have an account?\n1. Yes\t2. No\t3. Return\n', 'Italic/darkcyan'))
        self.ask_Acc_cust = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
        print()
        if self.ask_Acc_cust == "1":
            self.signin()
        elif self.ask_Acc_cust == "2" :
            print("Enter Your Details:")
            self.signup()
        elif self.ask_Acc_cust == "3" :
            self.begin()
        else:
            print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
            self.cust()
 ######################################################################################################   
    def owner(self):
        id = input("Enter your Username: ")
        passw = maskpass.askpass(prompt="Enter your Password:", mask="*")

        self.mycursor.execute('SELECT user, password FROM owner')
        for i in self.mycursor:
            if i[0] == id:
                if i[1] == passw:
                    self.ownerID = i[0]
                    self.ownerPASS = i[1]
                    self.OwnerWindow(d = 1)
                    break
                else:
                    print(fontstyle.apply("\nPassword is wrong!\n", 'Italic/red'))
                    print(fontstyle.apply('\nChoose:\n1. Return\n2. Retry', 'Italic/darkcyan'))
                    ask1 = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
                    if ask1 == "1":
                        self.begin()
                        break
                    elif ask1== '2':
                        self.owner()
                        break
                    else:
                        print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                        self.owner()
                        break
                    
        else:
            print(fontstyle.apply("\nNo Match Found!\n", 'Italic/red'))
            print(fontstyle.apply('\nChoose:\n1. Return\n2. Retry\n', 'Italic/darkcyan'))
            ask = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
            if ask == "1":
                self.begin()
            elif ask== '2':
                self.owner()
            else:
                print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                self.owner()
########################################################################################################
    def signin(self):
        id = input("Enter your Username: ")
        passw = maskpass.askpass(prompt="Enter your Password:", mask="*")
        self.mycursor.execute('SELECT username, password FROM customerpass')
        for i in self.mycursor:
            if i[0] == id:
                if i[1] == passw:
                    self.CustUSER = i[0]
                    self.CustWindow(d=1)
                    break
                else:
                    print(fontstyle.apply("\nPassword is wrong!\n", 'Italic/red'))
                    print(fontstyle.apply('\nChoose:\n1. Return\n2. Retry\n', 'Italic/darkcyan'))
                    ask = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
                    if ask == "1":
                        self.begin()
                        break
                    elif ask == '2':
                        self.signin()
                        break
                    else:
                        print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                        self.signin()
                        break
        else:
            print(fontstyle.apply("\nNo Match Found!\n", 'Italic/red'))
            print(fontstyle.apply('\nChoose:\n1. Return\n2. Retry\n', 'Italic/darkcyan'))
            ask = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
            if ask == "1":
                self.begin()
                
            elif ask == '2':
                self.signin()
            else:
                print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                self.signin()
#######################################################################################################            
    def signup(self):
        id = input("Enter your Username: ")
        passw = maskpass.askpass(prompt="Enter your Password:", mask="*")

        self.mycursor.execute('SELECT username FROM customerpass')

        for i in self.mycursor:
            if i[0] == id: 
                print(fontstyle.apply('Entered Username already exist, Do you want to sign in?\n1. Yes\t2. No\n3. Exit', 'Italic/darkcyan'))
                ask = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
                if ask == "1":
                    self.signin()
                    break
                elif ask == "2":
                    self.signup()
                    break
                else:
                    self.cust()
        else:
            self.mycursor.execute(f'insert into customerpass values("{id}","{passw}")')
            self.db.commit()
            nm = input("Enter your Name: ")
            phone = input("Enter your PhoneNo.: ")
            address = input("Enter your Address: ")
            self.mycursor.execute(f'insert into customerdet values("{nm}","{phone}", "{address}", "{id}")')
            self.db.commit()
            self.CustUSER = id
            self.CustWindow(d=1)
#######################################################################################################

    def CustWindow(self, d= 0):
        if d == 1:
            self.mycursor.execute(f'Select Name from customerdet where username = "{self.CustUSER}"')
            
            print(fontstyle.apply(f"\n{'🍴'*60}\n\t\t\tWelcome {[i[0] for i in self.mycursor][0]}! :)\n", 'Italic/cyan'))
        
        print(fontstyle.apply('\nChoose:\n1. Show Menu\n2. Place Order\n3. Exit', 'Italic/darkcyan'))
        ask = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
        if ask == "1":
            self.mycursor.execute('Select * from foods')
            z=[['Item Code', 'Name', 'Price(₹)']]
            c = 1
            for i in self.mycursor:
                z.append([c, i[0], i[1]])
                c+=1
            print('\n'*3,tabulate(z, headers='firstrow', tablefmt='fancy_grid'))
            print("\n")
            self.CustWindow()
        elif ask == "2":
            self.order()
        elif ask == "3":
            print(fontstyle.apply("\n\t\tThankYou\n", 'Italic/blue'))
            self.begin()
        else:
            
            print(fontstyle.apply("Wrong Input!", 'Italic/red'))
            self.CustWindow()
    def order(self):
        self.mycursor.execute('Select * from foods')
        foods = self.mycursor.fetchall()
        self.d = []
        while 1:
            ak = input("\n\nEnter the item code: ")
            qua = input("Enter its quantity: ")
            if ak and qua:
                try:
                    self.d.append([foods[int(ak)-1][0], int(qua), int(qua)*int(foods[int(ak)-1][1])])
                except:
                    print(fontstyle.apply("Wrong Input!", 'Italic/red'))
            print(fontstyle.apply('\nWould you like to add more items?\n1.Yes\t2. No\n', 'Italic/darkcyan'))      
            ed = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
            if ed == '2':
                if self.d:
                    self.bill()
                    break
                else:
                    self.d.clear()
                    self.CustWindow()
                    break
            elif ed !='1':
                print(fontstyle.apply("\nWrong Input!\n", 'Italic/red'))
    def bill(self):
        print('\n'*3)
        z = 0
        print(f'\tXYZ Pure Veg Restaurant\n\t\t{str(DT.datetime.now().strftime("%d/%m/%Y"))}\n\t\t{str(DT.datetime.now().strftime("%X"))}')
        for i in self.d:
            z+=i[2]
        self.d.extend([[],['', '_________________________', '_______'],['', 'Total', z]])

        self.mycursor.execute(f'Select * from customerdet where username = "{self.CustUSER}"')
        details = self.mycursor.fetchall()
        print(f'\nCustomer Name: {details[0][0]}\nAddress: {details[0][2]}\nPhone no.: {details[0][1]}')
        
        print(tabulate(self.d, headers = ['Item', 'Quantity', 'Price'], tablefmt="outline"))
        
        print(fontstyle.apply("\n\t\tThankyou for ordering!!", 'Italic/cyan'))
        self.CustWindow()

#######################################################################################################    
    def OwnerWindow(self, d = 0):
        if d == 1:
            print('\n\n','⟫⟪'*60)
            
            print(fontstyle.apply("\t\t\tWelcome Sir!!", 'bold/Italic/cyan'))
        print(fontstyle.apply('\n\nChoose:\n1. Show Menu\n2. Add an Item\n3. Remove an Item\n4. Update an Item\n5. Add an account\n6. Change login details\n7. Remove an account\n8. Exit\n', 'Italic/darkcyan'))
        ask = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
        if ask == "1":
            self.mycursor.execute('Select * from foods')
            z=[['Name', 'Price(₹)']]
            for i in self.mycursor:
                z.append(i)
            print('\n', tabulate(z, headers='firstrow', tablefmt='fancy_grid'))
            print("\n")
            self.OwnerWindow()
        
        elif ask == "2":
            self.additem()
                
        elif ask == "3":
            self.remove()
        elif ask == "4":
            self.update()
        elif ask == "5":
            self.addac()
        elif ask == "6":
            self.updatelogin()
        elif ask == "7":
            self.removeAcc()
        elif ask == '8':
            print(fontstyle.apply("\n\t\tThankYou\n", 'Italic/blue'))
            self.begin()
        else:
            
            print(fontstyle.apply("\nWrong Input!", 'Italic/red'))
            self.OwnerWindow()

    
    def additem(self):
        n = input("Enter the name of the item: ")
        p = int(input("Enter the price of the item: "))
        self.mycursor.execute(f"Insert into foods values('{n}','{p}')")
        self.db.commit()
        print(fontstyle.apply("Item added successfully!!\n", 'Italic/green'))
        
        print(fontstyle.apply('Add more items?\n1. Yes\t2. No\n', 'Italic/darkcyan'))
        z = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
        if z == "1":
            self.additem()
        elif z == '2':
            print()
            self.OwnerWindow()
        else:
            print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
            self.OwnerWindow()
    
    def remove(self):
        n = input("Enter the name of the item to remove: ")
        self.mycursor.execute(f'Delete from foods where Name = "{n}"')
        self.db.commit()
        print(fontstyle.apply("Item removed successfully!!\n", 'Italic/green'))
        
        print(fontstyle.apply('Remove more items?\n1. Yes\t2. No\n', 'Italic/darkcyan'))
        z = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
        if z == "1":
            self.remove()
        elif z == '2':
            print()
            self.OwnerWindow()
        else:
            print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
            self.OwnerWindow()

    def update(self):
        n = input("Enter the name of the item: ")
        p = int(input("Enter the new price: "))
        self.mycursor.execute(f'Update foods set Price = {p} where Name = "{n}"')
        self.db.commit()
        print(fontstyle.apply("Item updated successfully!!\n", 'Italic/green'))
        
        print(fontstyle.apply('Update more items?\n1. Yes\t2. No\n', 'Italic/darkcyan'))
        z = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
        if z == "1":
            self.update()
        elif z == '2':
            print()
            self.OwnerWindow()  
        else:
            print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
            self.OwnerWindow()

    def addac(self):
        id = input("Enter your Username: ")
        passw = maskpass.askpass(prompt="Enter your Password:", mask="*")

        self.mycursor.execute('SELECT user FROM owner')

        for i in self.mycursor:
            if i[0] == id:
                
                print(fontstyle.apply('Entered Username already exist, Do you want to return?\n1. Yes\t2. No\n', 'Italic/darkcyan'))
                ask = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
                if ask == "1":
                    self.OwnerWindow()
                    break
                elif ask == '2':
                    self.addac()
                    break
                else:
                    print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                    self.addac()
                    break
        else:
            self.mycursor.execute(f'insert into owner values("{id}","{passw}")')
            self.db.commit()
            print(fontstyle.apply("New account added successfully!!\n", 'Italic/green'))
            self.OwnerWindow()

    def updatelogin(self):
        ask = maskpass.askpass(prompt="Enter your old Password:", mask="*")
        if ask == self.ownerPASS:
            passw = maskpass.askpass(prompt="Enter new Password:", mask="*")

            self.mycursor.execute('SELECT user FROM owner')
            self.mycursor.execute(f'update owner set password = "{passw}" where user = "{self.ownerID}"')
            self.db.commit()
            print(fontstyle.apply("Password changed successfully!!\n", 'Italic/green'))
            self.OwnerWindow()
        else:
            
            print(fontstyle.apply("\nWrong Input!", 'Italic/red'))
            
            print(fontstyle.apply('Would you like to retry?\n1. Yes\t2. No\n', 'Italic/darkcyan'))
            tr = input(fontstyle.apply("Your Choice: ", 'Italic/purple'))
            if tr == "1":
                self.updatelogin()
            elif tr == '2':
                self.OwnerWindow()
            else:
                print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                self.OwnerWindow()
    
    def removeAcc(self):
        id = input("Enter that Username: ")
        passw = maskpass.askpass(prompt="Enter the Password:", mask="*")

        self.mycursor.execute('SELECT user, password FROM owner')
        for i in self.mycursor:
            if i[0] == id:
                if i[1] == passw:
                    self.mycursor.execute(f'delete from owner where user = "{id}"')
                    self.db.commit()
                    print(fontstyle.apply("Account removed successfully!!\n", 'Italic/green'))
                    self.OwnerWindow(d = 1)
                    break
                else:
                    print(fontstyle.apply("\nPassword is wrong!\n", 'Italic/red'))
                    print(fontstyle.apply('\nChoose:\n1. Return\n2. Retry', 'Italic/darkcyan'))
                    ask1 = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
                    if ask1 == "1":
                        self.begin()
                        break
                    elif ask == '2':
                        self.removeAcc()
                        break
                    else:
                        print(fontstyle.apply("Password changed successfully!!\n", 'Italic/green'))
                        self.removeAcc()
                        break

                    
        else:
            print(fontstyle.apply("\nNo Match Found!\n", 'Italic/red'))
            print(fontstyle.apply('\nChoose:\n1. Return\n2. Retry\n', 'Italic/darkcyan'))
            ask = input(fontstyle.apply("\nYour Choice: ", 'Italic/purple'))
            if ask == "1":
                self.begin()
            elif ask == '2':
                self.removeAcc()
            else:
                print(fontstyle.apply("\n\nWrong Input!\n", 'Italic/red'))
                self.removeAcc()

Manage().begin(d = 1)
