from datetime import datetime
from nicegui import ui
from src.ExpenseManager import ExpenseManager, ExpenseField


ExpenseTypes = {
    'transportation': 'Transportation',
    'accommodation': 'Accommodation',
    'food_drink': 'Food & Drink',
    'miscellaneous': 'Miscellaneous'
}


class ExpenseTable:
    def __init__(self, manager: ExpenseManager):
        self.manager = manager
        self.table = self._create_table()
        
    def _create_table(self):
        expenses = self.manager.get_expenses()
        columns = [
            {'name': 'expense_id', 'label': 'ID', 'field': 'expense_id', 'sortable': True},
            {'name': 'date', 'label': 'Date', 'field': 'date', 'sortable': True},
            {'name': 'expense_type', 'label': 'Type', 'field': 'expense_type', 'sortable': True},
            {'name': 'category', 'label': 'Category', 'field': 'category', 'sortable': True},
            {'name': 'amount', 'label': 'Amount', 'field': 'amount', 'sortable': True},
            {'name': 'currency', 'label': 'Currency', 'field': 'currency', 'sortable': True},
            {'name': 'location', 'label': 'Location', 'field': 'location', 'sortable': True},
            {'name': 'receipt', 'label': 'Receipt', 'field': 'receipt', 'sortable': True},
            {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
            {'name': 'reimbursement_status', 'label': 'Status', 'field': 'reimbursement_status', 'sortable': True},
            {'name': 'additional_notes', 'label': 'Notes', 'field': 'additional_notes', 'sortable': True},
        ]
        rows = [
            {
                'expense_id': expense[0],
                'date': expense[1],
                'expense_type': expense[2],
                'category': expense[3],
                'amount': expense[4],
                'currency': expense[5],
                'location': expense[6],
                'receipt': expense[7],
                'email': expense[8],
                'reimbursement_status': expense[9],
                'additional_notes': expense[10],
            }
            for expense in expenses
        ]

        return ui.table(columns=columns, rows=rows, row_key='expense_id').classes('w-full')
        
    def add_expense(self, date, expense_type, category, amount, currency, location, receipt, email, reimbursement_status, additional_notes):
        expense_id = self.manager.add_expense(date, expense_type, category, amount, currency, location, receipt, email, reimbursement_status, additional_notes)
        self.table.add_rows({
            'expense_id': expense_id,
            'date': date,
            'expense_type': expense_type,
            'category': category,
            'amount': amount,
            'currency': currency,
            'location': location,
            'receipt': receipt,
            'email': email,
            'reimbursement_status': reimbursement_status,
            'additional_notes': additional_notes
        })
        self.table.run_method('scrollTo', len(self.table.rows) - 1)

class Expense:
    def __init__(self, date=None, expense_type=None, category=None, amount=None, currency=None, location=None, receipt=None, email=None, reimbursement_status=None, additional_notes=None):
        self.date = date
        self.expense_type = expense_type
        self.category = category
        self.amount = amount
        self.currency = currency
        self.location = location
        self.receipt = receipt
        self.email = email
        self.reimbursement_status = reimbursement_status
        self.additional_notes = additional_notes

    def set_date(self, date):
        self.date = date

    def set_expense_type(self, expense_type):
        self.expense_type = expense_type

    def set_amount(self, amount):
        self.amount = amount

    def set_currency(self, currency):
        self.currency = currency

    def set_location(self, location):
        self.location = location

    def set_receipt(self, receipt):
        self.receipt = receipt

    def set_email(self, email):
        self.email = email

    def set_reimbursement_status(self, reimbursement_status):
        self.reimbursement_status = reimbursement_status

    def set_additional_notes(self, additional_notes):
        self.additional_notes = additional_notes


def create_expense_dialog():
    expense = Expense()

    with ui.dialog() as expense_dialog, ui.card():

        # Date
        today = datetime.today().strftime('%Y-%m-%d')
        with ui.input('Date').bind_value_to(globals(), 'date_value') as date:
            with ui.menu().props('no-parent-event') as date_menu:
                with ui.date(value=today).bind_value_to(date):
                    with ui.row().classes('justify-end'):
                        ui.button('Close', on_click=date_menu.close).props('flat')
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', date_menu.open).classes('cursor-pointer')

        # Expense Type
        expense_type = ui.select(options = ExpenseTypes, label='Expense Type', value='transportation').classes('w-full')

        with ui.row():
            # Amount
            amount = ui.number(label='Amount', format='%.2f', prefix='$', value=0.00, step=0.01)

            # Currency
            currency = ui.select(options = {'usd': 'USD', 'eur': 'EUR', 'gbp': 'GBP'}, label='Currency', value='usd')

        # Submit or Cancel
        with ui.row():
            submit = ui.button('Submit', on_click=expense_dialog.close)
            submit.on_click(lambda: expense.set_date(date_value))
            submit.on_click(lambda: expense.set_expense_type(expense_type.value))
            submit.on_click(lambda: expense.set_amount(amount.value))
            submit.on_click(lambda: expense.set_currency(currency.value))
            ui.button('Cancel', on_click=lambda: expense_dialog.submit(False))
    
    return expense_dialog, expense


async def show_add_expense():
    expense_dialog, expense = create_expense_dialog()
    
    result = await expense_dialog
    if result == False:
        ui.notify('Expense not added')
    else:
        ui.notify('Expense added')
        for attribute, value in expense.__dict__.items():
            print(f"{attribute}: {value}")

    expense_dialog.close()
    expense_dialog.clear()



if __name__ in {"__main__", "__mp_main__"}:
    ui.dark_mode(True)

    manager = ExpenseManager()
    expense_table = ExpenseTable(manager)

    ui.button('Add Expense', on_click=show_add_expense)



    ui.run()