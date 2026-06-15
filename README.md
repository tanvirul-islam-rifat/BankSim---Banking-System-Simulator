# BankSim — Banking System Simulator

A command-line banking simulator built entirely in Python using Object-Oriented Programming. Supports two account types — Savings and Current — with full transaction operations, interest calculation, overdraft handling, and persistent data storage.


---

## Features

- **Create Accounts** — Open a Savings or Current account with an initial deposit
- **Deposit & Withdraw** — Standard transactions with balance validation
- **Transfer Funds** — Move money between any two accounts
- **Interest Application** — Apply 6% annual interest to Savings accounts
- **Overdraft Support** — Current accounts allow withdrawals up to ৳10,000 beyond balance
- **Transaction History** — Full timestamped log of every operation per account
- **Persistent Storage** — All accounts and transactions survive across sessions via file I/O

---

## OOP Design

```
Account  (Base Class)
├── SavingsAccount   — inherits Account; adds interest rate, apply_interest()
└── CurrentAccount   — inherits Account; overrides withdraw() with overdraft logic

Bank                 — aggregates all Account objects; manages persistence & operations
```

| OOP Concept | Where Applied |
|---|---|
| **Encapsulation** | Private attributes (`__balance`, `__account_number`) with getters |
| **Inheritance** | `SavingsAccount` and `CurrentAccount` extend `Account` |
| **Polymorphism** | `withdraw()` and `get_info()` behave differently per account type |
| **Abstraction** | `Bank` class hides all file I/O and internal logic from the menu |

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/YourGitHubUsername/banksim-banking-system.git
cd banksim-banking-system

# Run the application (Python 3 required, no external libraries needed)
python3 banksim.py
```

---

## Sample Session

```
Welcome to BankSim National Bank

=============================================
        BankSim — Banking Simulator
=============================================
  1. Create New Account
  2. View Account Details
  3. Deposit Money
  4. Withdraw Money
  5. Transfer Between Accounts
  6. Apply Interest (Savings only)
  7. View Transaction History
  8. List All Accounts
  9. Exit
=============================================
Enter your choice (1-9): 1

-- Create New Account --
Enter account holder name: Tanvir
Account type:
  1. Savings (6% interest, no overdraft)
  2. Current (no interest, ৳10,000 overdraft)
Choose (1/2): 1
Initial deposit (৳): 5000

Account created successfully!
Account Number : 10000001
Account Type   : Savings
```

---

## Project Structure

```
banksim-banking-system/
├── banksim.py          # Main application — all classes and CLI
├── data/
│   ├── accounts.txt    # Persisted account records (auto-generated)
│   └── transactions.txt # Full transaction log (auto-generated)
└── README.md
```

---

## Technical Architecture

- **Language:** Python 3.x
- **Paradigm:** Object-Oriented Programming (OOP)
- **Data Storage:** Flat-file text database (`.txt`) with dynamic serialization and deserialization
- **Interface:** Command Line Interface (CLI)

## Core Engineering Practices Demonstrated

- **OOP Design Patterns:** Three-layer class hierarchy (`Account` → `SavingsAccount` / `CurrentAccount` → `Bank`) with clear separation of concerns
- **Encapsulation:** All sensitive financial data protected via private attributes; only exposed through controlled getter methods
- **Polymorphic Overriding:** `CurrentAccount.withdraw()` overrides the base class to implement overdraft logic without modifying the parent class
- **Aggregation:** The `Bank` class manages a dictionary of `Account` objects, demonstrating object composition
- **Persistent Logging:** Every financial transaction is timestamped and written to a separate log file for full auditability
- **Defensive Programming:** All monetary inputs validated with type checking and boundary enforcement before any state change

## Author

**Md. Tanvirul Islam Rifat**

* **GitHub:** [@tanvirul-islam-rifat](https://github.com/tanvirul-islam-rifat)
* **LinkedIn:** [Tanvirul Islam Rifat](https://www.linkedin.com/in/tanvirul-islam-rifat)
