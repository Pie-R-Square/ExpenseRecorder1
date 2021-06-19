import sqlite3

# create data base
conn = sqlite3.connect('Expense.db')

# create operater
c = conn.cursor()

# create table
'''
 'Details(details)'
'Rate(rate)'
'Quantity(quantity)'
'Discount(discount)'
'Total(amount)'
'Timestamp(now)'
'Transaction ID(transactionID)'
'''
c.execute("""CREATE TABLE IF NOT EXISTS ExpenseList(
					ID INTEGER PRIMARY KEY AUTOINCREMENT,
					details TEXT,
					rate REAL,
					quantity REAL,
					discount REAL,
					amount REAL,
					now TEXT,
					transactionID TEXT
				)""")
def insert_expense(details, rate, quantity, discount, amount, now, transactionID):
	ID = None
	with conn:
		c.execute("""INSERT INTO expenseList VALUES (?,?,?,?,?,?,?,?)""",
			(ID, details, rate, quantity, discount, amount, now, transactionID))
		conn.commit() # record data to database
		print("Insert succeed")

def show_expense():
	with conn:
		c.execute("SELECT * FROM expenseList")
		expense = c.fetchall()
		print(expense)

	return expense

show_expense()

#insert_expense("f",52.0,15.0,4468.0,-3688.0,"Jun 12, 2021 20:35:53",202106122035757644)

print("Succeed")