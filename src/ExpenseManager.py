import sqlite3
from datetime import datetime
from enum import Enum

class ExpenseField(Enum):
    DATE = 'date'
    EXPENSE_TYPE = 'expense_type'
    CATEGORY = 'category'
    AMOUNT = 'amount'
    CURRENCY = 'currency'
    LOCATION = 'location'
    RECEIPT = 'receipt'
    EMAIL = 'email'
    REIMBURSEMENT_STATUS = 'reimbursement_status'
    ADDITIONAL_NOTES = 'additional_notes'

class ExpenseManager:
    def __init__(self, db_path='database/work_expenses.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            expense_type TEXT,
            amount REAL,
            currency TEXT,
            location TEXT,
            receipt BLOB,
            email TEXT,
            reimbursement_status TEXT,
            additional_notes TEXT
        )
        ''')
        self.conn.commit()

    def add_expense(self, date, expense_type, amount, currency, location, receipt, email, reimbursement_status, additional_notes):
        self.cursor.execute('''
        INSERT INTO expenses (date, expense_type, amount, currency, location, receipt, email, reimbursement_status, additional_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, expense_type, amount, currency, location, receipt, email, reimbursement_status, additional_notes))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_expense(self, expense_id, update_fields):
        if not update_fields:
            return
        fields = ", ".join(f"{field.value} = ?" for field in update_fields.keys())
        values = list(update_fields.values())
        values.append(expense_id)
        query = f"UPDATE expenses SET {fields} WHERE expense_id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute('''
        DELETE FROM expenses
        WHERE expense_id = ?
        ''', (expense_id,))
        self.conn.commit()

    def get_expenses(self):
        self.cursor.execute('SELECT * FROM expenses')
        return self.cursor.fetchall()

    def get_expense(self, expense_id):
        self.cursor.execute('SELECT * FROM expenses WHERE expense_id = ?', (expense_id,))
        return self.cursor.fetchone()

    def erase_all_expenses(self):
        self.cursor.execute('DELETE FROM expenses')
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    manager = ExpenseManager()
    new_expense_data = (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Transportation',
        25.50,
        'USD',
        'New York',
        None,
        'example@example.com',
        'Pending',
        'Trip to client meeting'
    )
    expense_id = manager.add_expense(*new_expense_data)
    print(f"New expense ID: {expense_id}")

    manager.update_expense(expense_id, {
        ExpenseField.AMOUNT: 30.00,
        ExpenseField.REIMBURSEMENT_STATUS: 'Approved'
    })

    expenses = manager.get_expenses()
    for expense in expenses:
        print(expense)

    # Erase all expenses
    manager.erase_all_expenses()
    print("All expenses erased.")

    manager.close()
