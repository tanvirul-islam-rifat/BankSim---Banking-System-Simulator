"""
BankSim - Banking System Simulator
An OOP-based CLI application simulating core banking operations including
account management, transactions, and interest calculation.

Course: CSE111 - Programming Language II
"""

import os
import datetime

DATA_FILE = "data/accounts.txt"
TRANSACTION_FILE = "data/transactions.txt"


# ─────────────────────────────────────────────
# BASE CLASS
# ─────────────────────────────────────────────

class Account:
    """Base class representing a generic bank account."""

    def __init__(self, account_number, owner_name, balance=0.0):
        self.__account_number = account_number   # Encapsulation: private
        self.__owner_name = owner_name
        self.__balance = float(balance)

    # Getters
    def get_account_number(self):
        return self.__account_number

    def get_owner_name(self):
        return self.__owner_name

    def get_balance(self):
        return self.__balance

    def get_account_type(self):
        return "Generic"

    # Protected setter for subclasses
    def _set_balance(self, amount):
        self.__balance = amount

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be greater than zero."
        self.__balance += amount
        return True, f"Deposited ৳{amount:.2f} successfully."

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        if amount > self.__balance:
            return False, "Insufficient balance."
        self.__balance -= amount
        return True, f"Withdrawn ৳{amount:.2f} successfully."

    def get_info(self):
        return (
            f"Account No : {self.__account_number}\n"
            f"Owner      : {self.__owner_name}\n"
            f"Type       : {self.get_account_type()}\n"
            f"Balance    : ৳{self.__balance:.2f}"
        )

    def to_file_string(self):
        """Serialize account data to a string for file storage."""
        return f"{self.get_account_type()},{self.__account_number},{self.__owner_name},{self.__balance:.2f}"


# ─────────────────────────────────────────────
# SUBCLASS 1: SAVINGS ACCOUNT
# ─────────────────────────────────────────────

class SavingsAccount(Account):
    """Savings account with an annual interest rate."""

    INTEREST_RATE = 0.06   # 6% annual interest

    def __init__(self, account_number, owner_name, balance=0.0):
        super().__init__(account_number, owner_name, balance)

    def get_account_type(self):
        return "Savings"

    def apply_interest(self):
        """Apply annual interest to the current balance."""
        interest = self.get_balance() * self.INTEREST_RATE
        self._set_balance(self.get_balance() + interest)
        return interest

    def get_info(self):
        return super().get_info() + f"\nInt. Rate  : {self.INTEREST_RATE * 100:.0f}% per annum"


# ─────────────────────────────────────────────
# SUBCLASS 2: CURRENT ACCOUNT
# ─────────────────────────────────────────────

class CurrentAccount(Account):
    """Current account with an overdraft limit for businesses."""

    OVERDRAFT_LIMIT = 10000.0

    def __init__(self, account_number, owner_name, balance=0.0):
        super().__init__(account_number, owner_name, balance)

    def get_account_type(self):
        return "Current"

    def withdraw(self, amount):
        """Override withdrawal to allow overdraft up to the limit."""
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        if amount > self.get_balance() + self.OVERDRAFT_LIMIT:
            return False, f"Exceeds overdraft limit of ৳{self.OVERDRAFT_LIMIT:.2f}."
        self._set_balance(self.get_balance() - amount)
        return True, f"Withdrawn ৳{amount:.2f} successfully."

    def get_info(self):
        return super().get_info() + f"\nOverdraft  : ৳{self.OVERDRAFT_LIMIT:.2f} limit"


# ─────────────────────────────────────────────
# BANK CLASS (Manages everything)
# ─────────────────────────────────────────────

class Bank:
    """Core banking engine managing all accounts and transactions."""

    def __init__(self, name):
        self.name = name
        self.__accounts = {}   # account_number -> Account object
        self.__transactions = []
        self.__load_accounts()
        self.__load_transactions()

    def __generate_account_number(self):
        existing = [int(k) for k in self.__accounts.keys() if k.isdigit()]
        return str(10000001 + len(existing)).zfill(8)

    def __log_transaction(self, account_number, transaction_type, amount, note=""):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp},{account_number},{transaction_type},{amount:.2f},{note}"
        self.__transactions.append(entry)
        self.__save_transactions()

    # ── Persistence ──

    def __load_accounts(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                acc_type, acc_no, name, balance = parts[0], parts[1], parts[2], float(parts[3])
                if acc_type == "Savings":
                    self.__accounts[acc_no] = SavingsAccount(acc_no, name, balance)
                elif acc_type == "Current":
                    self.__accounts[acc_no] = CurrentAccount(acc_no, name, balance)

    def __save_accounts(self):
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            for acc in self.__accounts.values():
                f.write(acc.to_file_string() + "\n")

    def __load_transactions(self):
        if not os.path.exists(TRANSACTION_FILE):
            return
        with open(TRANSACTION_FILE, "r") as f:
            self.__transactions = [line.strip() for line in f if line.strip()]

    def __save_transactions(self):
        os.makedirs("data", exist_ok=True)
        with open(TRANSACTION_FILE, "w") as f:
            for entry in self.__transactions:
                f.write(entry + "\n")

    # ── Public Operations ──

    def create_account(self, owner_name, account_type, initial_deposit=0.0):
        acc_no = self.__generate_account_number()
        if account_type == "1":
            account = SavingsAccount(acc_no, owner_name, initial_deposit)
        else:
            account = CurrentAccount(acc_no, owner_name, initial_deposit)
        self.__accounts[acc_no] = account
        self.__save_accounts()
        if initial_deposit > 0:
            self.__log_transaction(acc_no, "INITIAL DEPOSIT", initial_deposit)
        return acc_no, account.get_account_type()

    def get_account(self, acc_no):
        return self.__accounts.get(acc_no, None)

    def deposit(self, acc_no, amount):
        account = self.get_account(acc_no)
        if not account:
            return False, "Account not found."
        success, msg = account.deposit(amount)
        if success:
            self.__save_accounts()
            self.__log_transaction(acc_no, "DEPOSIT", amount)
        return success, msg

    def withdraw(self, acc_no, amount):
        account = self.get_account(acc_no)
        if not account:
            return False, "Account not found."
        success, msg = account.withdraw(amount)
        if success:
            self.__save_accounts()
            self.__log_transaction(acc_no, "WITHDRAWAL", amount)
        return success, msg

    def transfer(self, from_acc, to_acc, amount):
        sender = self.get_account(from_acc)
        receiver = self.get_account(to_acc)
        if not sender:
            return False, "Sender account not found."
        if not receiver:
            return False, "Receiver account not found."
        success, msg = sender.withdraw(amount)
        if success:
            receiver.deposit(amount)
            self.__save_accounts()
            self.__log_transaction(from_acc, "TRANSFER OUT", amount, f"to {to_acc}")
            self.__log_transaction(to_acc, "TRANSFER IN", amount, f"from {from_acc}")
            return True, f"৳{amount:.2f} transferred successfully."
        return False, msg

    def apply_interest(self, acc_no):
        account = self.get_account(acc_no)
        if not account:
            return False, "Account not found."
        if not isinstance(account, SavingsAccount):
            return False, "Interest only applies to Savings accounts."
        interest = account.apply_interest()
        self.__save_accounts()
        self.__log_transaction(acc_no, "INTEREST", interest)
        return True, f"Interest of ৳{interest:.2f} applied at 6% per annum."

    def get_transaction_history(self, acc_no):
        history = [t for t in self.__transactions if t.split(",")[1] == acc_no]
        return history

    def list_all_accounts(self):
        return list(self.__accounts.values())


# ─────────────────────────────────────────────
# CLI MENU
# ─────────────────────────────────────────────

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def print_menu():
    print("\n" + "=" * 45)
    print("        BankSim — Banking Simulator")
    print("=" * 45)
    print("  1. Create New Account")
    print("  2. View Account Details")
    print("  3. Deposit Money")
    print("  4. Withdraw Money")
    print("  5. Transfer Between Accounts")
    print("  6. Apply Interest (Savings only)")
    print("  7. View Transaction History")
    print("  8. List All Accounts")
    print("  9. Exit")
    print("=" * 45)


def main():
    os.makedirs("data", exist_ok=True)
    bank = Bank("BankSim National Bank")
    print(f"\nWelcome to {bank.name}")

    while True:
        print_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            print("\n-- Create New Account --")
            name = input("Enter account holder name: ").strip()
            print("Account type:\n  1. Savings (6% interest, no overdraft)\n  2. Current (no interest, ৳10,000 overdraft)")
            acc_type = input("Choose (1/2): ").strip()
            if acc_type not in ["1", "2"]:
                print("Invalid choice.")
                continue
            initial = get_float_input("Initial deposit (৳): ")
            acc_no, acc_type_name = bank.create_account(name, acc_type, initial)
            print(f"\nAccount created successfully!")
            print(f"Account Number : {acc_no}")
            print(f"Account Type   : {acc_type_name}")

        elif choice == "2":
            acc_no = input("\nEnter Account Number: ").strip()
            account = bank.get_account(acc_no)
            if account:
                print("\n" + account.get_info())
            else:
                print("Account not found.")

        elif choice == "3":
            acc_no = input("\nEnter Account Number: ").strip()
            amount = get_float_input("Enter deposit amount (৳): ")
            success, msg = bank.deposit(acc_no, amount)
            print(msg)

        elif choice == "4":
            acc_no = input("\nEnter Account Number: ").strip()
            amount = get_float_input("Enter withdrawal amount (৳): ")
            success, msg = bank.withdraw(acc_no, amount)
            print(msg)

        elif choice == "5":
            print("\n-- Transfer Money --")
            from_acc = input("From Account Number: ").strip()
            to_acc = input("To Account Number  : ").strip()
            amount = get_float_input("Amount to transfer (৳): ")
            success, msg = bank.transfer(from_acc, to_acc, amount)
            print(msg)

        elif choice == "6":
            acc_no = input("\nEnter Savings Account Number: ").strip()
            success, msg = bank.apply_interest(acc_no)
            print(msg)

        elif choice == "7":
            acc_no = input("\nEnter Account Number: ").strip()
            history = bank.get_transaction_history(acc_no)
            if not history:
                print("No transactions found for this account.")
            else:
                print(f"\n{'Timestamp':<22}{'Type':<18}{'Amount':>10}  Note")
                print("-" * 60)
                for entry in history:
                    parts = entry.split(",")
                    note = parts[4] if len(parts) > 4 else ""
                    print(f"{parts[0]:<22}{parts[2]:<18}৳{float(parts[3]):>9.2f}  {note}")

        elif choice == "8":
            accounts = bank.list_all_accounts()
            if not accounts:
                print("\nNo accounts found.")
            else:
                print(f"\n{'Acc No':<12}{'Owner':<20}{'Type':<10}{'Balance':>12}")
                print("-" * 56)
                for acc in accounts:
                    print(f"{acc.get_account_number():<12}{acc.get_owner_name():<20}{acc.get_account_type():<10}৳{acc.get_balance():>10.2f}")

        elif choice == "9":
            print("\nThank you for using BankSim. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
