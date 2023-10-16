class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.loan_taken = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited: +{amount}")
        return f"Deposited: {amount}"

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew: -{amount}")
            return f"Withdrew: {amount}"
        else:
            return "Withdrawal amount exceeded"

    def check_balance(self):
        return f"Available balance: {self.balance}"

    def transfer(self, receiver, amount):
        if receiver:
            if amount <= self.balance:
                self.balance -= amount
                for user in admin.get_all_accounts():
                    if user.name == receiver:
                        user.balance += amount
                        self.transactions.append(
                            f"Transferred: -{amount} to {user.name}"
                        )
                        user.transactions.append(
                            f"Received: +{amount} from {self.name}"
                        )
                        return f"Transferred {amount} to {user.name}"
            else:
                return "Insufficient balance for transfer"
        else:
            return "Recipient account does not exist"

    def take_loan(self, amount):
        if self.loan_taken < 2 and Admin.loan_status:
            self.balance += amount
            self.loan_taken += 1
            Admin.total_loan += amount
            self.transactions.append(f"Loan taken: +{amount}")
            return f"Loan of {amount} granted"
        else:
            return "You have reached the maximum limit for taking a loan"

    def transaction_history(self):
        return self.transactions


class Admin:
    total_balance = 0
    total_loan = 0
    loan_status = True
    account_list = []

    def __init__(self, name, email):
        self.users = []
        self.name = name
        self.email = email

    def create_account(self, name, email, address, account_type):
        new_user = User(name, email, address, account_type)
        self.users.append(new_user)
        return new_user

    def delete_account(self, user):
        self.users.remove(user)

    def get_all_accounts(self):
        return self.users

    def show_total_balance(self):
        total_balance = sum(user.balance for user in self.users)
        print(f"Total available balance in the bank: ${total_balance}")

    def total_loan_amount(self):
        total_loan = Admin.total_loan
        print(f"Total loan from the bank: ${total_loan}")

    def off_loan(self):
        Admin.loan_status = False
        print("Loan Services is Off for Now")

    def on_loan(self):
        Admin.loan_status = True
        print("Loan Services is On")


admin = Admin("admin", "admin@gmail.com")
user1 = admin.create_account("John Doe", "john@example.com", "123 Main St", "Savings")
user2 = admin.create_account("user2", "user2@gmail.com", "address2", "savings")

print(user1.deposit(1000))
print(user2.deposit(1500))
print(user1.check_balance())
print(user2.check_balance())
print(user1.transfer(user2, 500))
print(user1.check_balance())
print(user2.check_balance())
print(user1.take_loan(2000))
print(user1.take_loan(5000))

while True:
    try:
        print("1. User? ")
        print("2. Admin? ")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            print("\n-----User-----")
            user_name = input("name: ")
            user_email = input("email: ")
            user_address = input("address: ")
            user_type = input("account type (Savings/Current): ")
            user_account = admin.create_account(
                user_name, user_email, user_address, user_type
            )
            while True:
                print("\nUser Menu")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Check Transaction History")
                print("5. Take Loan")
                print("6. Transfer Money")
                user_choice = input("Select an option: ")
                if user_choice == "1":
                    amount = float(input("Enter the deposit amount: $"))
                    print(user_account.deposit(amount))
                elif user_choice == "2":
                    amount = float(input("Enter the withdrawal amount: $"))
                    print(user_account.withdraw(amount))
                elif user_choice == "3":
                    print(f"${user_account.check_balance()}")
                elif user_choice == "4":
                    print("\nTransaction History:")
                    for transaction in user_account.transaction_history():
                        print(transaction)
                elif user_choice == "5":
                    loan_amount = float(input("Enter the loan amount: $"))
                    user_account.take_loan(loan_amount)
                elif user_choice == "6":
                    receiver = input("Receiver user name: ")
                    if receiver:
                        amount = float(input("Enter the transfer amount: $"))
                        user_account.transfer(receiver, amount)
                    else:
                        print("account does not exist.")
                else:
                    print("Invalid Option")
        elif choice == "2":
            while True:
                print("\nAdmin Menu")
                print("1. Create User Account")
                print("2. Delete User Account")
                print("3. List User Accounts")
                print("4. Total Bank Balance")
                print("5. Total Loan Amount")
                print("6. Off Loan service")
                print("7. ON Loan service")
                print("8. Exit")
                admin_choice = input("Select an option: ")
                if admin_choice == "1":
                    try:
                        user_name = input("Enter user's name: ")
                        user_email = input("Enter user's email: ")
                        user_address = input("Enter user's address: ")
                        user_type = input("Enter account type (Savings/Current): ")
                        admin.create_account(
                            user_name,
                            user_email,
                            user_address,
                            user_type,
                        )
                    except ValueError:
                        print("Invalid Option! Please enter a number.")
                        continue
                elif admin_choice == "2":
                    try:
                        user_to_delete = input("name: ")
                        if user_to_delete:
                            admin.delete_account(user_to_delete)
                            print(f"User ID {user_to_delete} deleted.")
                        else:
                            print("User not found.")
                    except ValueError:
                        print("Invalid Option!")
                        continue
                elif admin_choice == "3":
                    try:
                        print("\nUser Accounts:")
                        for user in admin.get_all_accounts():
                            print(
                                [user.name, user.email, user.address, user.account_type]
                            )
                    except ValueError:
                        print("Invalid Option! Please enter a number.")
                        continue
                elif admin_choice == "4":
                    admin.show_total_balance()
                elif admin_choice == "5":
                    admin.total_loan_amount()
                elif admin_choice == "6":
                    admin.off_loan()
                elif admin_choice == "7":
                    admin.on_loan()
                elif admin_choice == "8":
                    break
        elif choice == "3":
            print("Thank you for your time. Have a great day")
            break
    except ValueError:
        print("Invalid Option! Please enter a number.")
        continue

