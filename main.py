import json
import random
import string
from pathlib import Path

class Bank:
    database= 'data.json'
    data=[]    #dummy data to store the data in the list and then update the json file
    try: 
        if Path(database).exists():
            with open(database) as file:
                data=json.load(file)
        else:
            print("no such file exists")
    except Exception as e:
        print(f"an exception occured as {e}")

    @classmethod
    def __update(cls):
        with open(Bank.database,'w') as file:
            file.write(json.dumps(Bank.data))
    @classmethod
    def __accountgenerate(cls):
        alpha= random.choices(string.ascii_letters, k=3)
        num= random.choices(string.digits, k=7)
        spchar= random.choices("!@#$%^&*()-+", k=2)
        id= alpha+num+spchar
        random.shuffle(id)
        return "".join(id)
#1----------------------------------------   
    def createAccount(self):
        info={
            "name": input("enter your name:"),
            "age": int(input("enter your age:")),
            "email": input("enter your email:"),
            "pin": int(input("enter your 4 digit pin:")),
            "account_number": Bank.__accountgenerate(),
            "balance": 0
        }
        if info['age']<18 or len(str(info['pin']))!=4:
            print("you are not eligible to create an account")
        else:
            print("account created successfully")
            for i in info:
                print(f"{i}:{info[i]}")
            print("please remember your account number and pin for future use")
            Bank.data.append(info)
            Bank.__update()

#2----------------------------------------          
    def depositMoney(self):
        acc_num=input("enter your account number:")
        pin=int(input("enter the pin aswell"))
        print(Bank.data)
        userdata= [i for i in Bank.data if i['account_number']==acc_num and i['pin']==pin]
        if userdata==False:
            print("invalid account number or pin")
        else:
            amount=int(input("enter the amount you want to deposit:"))
            if amount>10000 or amount<0:
                print("you cannot deposit this amount")
            else:
                print(userdata)
                userdata[0]['balance']+=amount
                Bank.__update()
                print("money deposited successfully")
                print(f"your current balance is {userdata[0]['balance']}")

#3----------------------------------------
    def withdrawMoney(self):
        acc_num=input("enter your account number:")
        pin=int(input("enter the pin aswell"))
        userdata= [i for i in Bank.data if i['account_number']==acc_num and i['pin']==pin]
        if userdata==False:
            print("invalid account number or pin")
        else:
            amount=int(input("enter the amount you want to withdraw:"))
            if amount>userdata[0]['balance'] or amount<0:
                print("you cannot withdraw this amount")
            else:
                userdata[0]['balance']-=amount
                Bank.__update()
                print("money withdrawn successfully")
                print(f"your current balance is {userdata[0]['balance']}")

#4----------------------------------------
    def showDetails(self):
        acc_num= input ("enter your account number:")
        pin=int(input("enter pin"))

        userdata= [i for i in Bank.data if i['account_number']==acc_num and i['pin']==pin]
        if userdata==False:
            print("no data found")
        else:
            print("your details are as follows:")
            for i in userdata[0]:
                print(f"{i}:{userdata[0][i]}")

# 5----------------------------------------
    def updateDetails(self):
        acc_num= input("enter account number")
        pin=int(input("enter the pin"))

        userdata=[i for i in Bank.data if i['account_number']==acc_num and i['pin']==pin]

        if userdata==False:
            print("no data found")
        else:
            print("what do you want to update")
            print("Note:- ypu cannot change age, account number and balance")
            print("press 1 for name")
            print("press 2 for email")
            print("press 3 for pin")
            check=int(input("enter your response:"))
            if check==1:
                new_name=input("enter your new name:")
                userdata[0]['name']=new_name
                Bank.__update()
                print("name updated successfully")
            elif check==2:
                new_email=input("enter your new email:")
                userdata[0]['email']=new_email
                Bank.__update()
                print("email updated successfully")
            elif check==3:
                new_pin=int(input("enter your new pin:"))
                userdata[0]['pin']=new_pin
                Bank.__update()
                print("pin updated successfully")
            else:
                print("invalid response")


# 6----------------------------------------
    def deleteAcc(self):
        acc_num= input("enter account number")
        pin=int(input("enter the pin"))

        userdata=[i for i in Bank.data if i['account_number']==acc_num and i['pin']==pin]

        if userdata==False:
            print("no data found")
        else:
            check=input("are you sure you want to delete your account? (y/n)")
            if check=="n" or check=="N":
                print("account deletion cancelled")
            elif check=="y" or check=="Y":
                index= Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully")



print("press 1 for creating an account")
print("press 2 for depositing money into the bank")
print("press 3 for withdrawing the money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting the account")

check= int(input("enter your response:"))

user = Bank()
if check==1:
    user.createAccount()

if check==2:
    user.depositMoney()

if check==3:
    user.withdrawMoney()

if check==4:
    user.showDetails()

if check==5:
    user.updateDetails()

if check==6:
    user.deleteAcc()
 