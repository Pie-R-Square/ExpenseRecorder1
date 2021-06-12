from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('Expense Record')
#GUI.geometry('1200x650+0+30')

#GUI.geometry('650x750+1000+100')

w = 1200
h = 650

ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen height


x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


############MENU##############

menubar = Menu(GUI)
GUI.config(menu=menubar)


file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='file', menu=file_menu)
file_menu.add_command(label='Import CSV')
file_menu.add_command(label='Export to Google Sheets')

help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='help', menu=help_menu)
help_menu.add_command(label='About')

##############################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

icon_T1 = PhotoImage(file='Images/Add-icon.png')
icon_T2 = PhotoImage(file='Images/Wallet-icon.png')

Tab.add(T1, text=f'{"Add Expense":^{15}}',image=icon_T1,compound='top')
Tab.add(T2, text=f'{"Expense List":^{15}}',image=icon_T2,compound='top')

#################################Tab 1#################################

F1 = Frame(T1)
#F1.place(x=100,y=50)
F1.pack()

days = {"Mon":"จันทร์",
		"Tue":"อังคาร",
		"Wed":"พุธ",
		"Thu":"พฤหัส",
		"Fri":"ศุกร์",
		"Sat":"เสาว์",
		"Sun":"อาทิตย์"}

def Save(event=None):
	details = v_details.get()
	rate = v_rate.get()
	quantity = v_quantity.get()
	discount = v_discount.get()

	if details == "":
		#print("No data")
		messagebox.showerror("ERROR","Please enter details!")
		return
	if rate == "":
		messagebox.showerror("ERROR","You typed wrong, please enter rate again!")
		return
	if quantity == "":
		quantity = 1
	if discount == "":
		discount = 0

	try:
		amount = float(rate)*float(quantity)-float(discount)
		now = datetime.now().strftime('%b %d, %Y %H:%M:%S')
		stamp = datetime.now()
		transactionID = stamp.strftime('%Y%m%d%H%M%f')
		compound_rt_text = '  Details: {}\n     Rate: {} ฿\n Quantity: {}\n Discount: {} ฿\n__________\n   Amount: {} ฿\nTimestamp: {}\n'.format(details,str(rate),str(quantity),str(discount),str(amount),now)
		compound_lt_text = 'Details: {}\nRate: {} ฿\nQuantity {}\nDiscount {} ฿\n__________\nAmount: {} ฿\nTimestamp: {}\n'.format(details,str(rate),str(quantity),str(discount),str(amount),now)
		print(compound_rt_text)
		v_result.set(compound_lt_text)
		v_details.set('')
		v_rate.set('')
		v_quantity.set('')
		v_discount.set('')

		with open('Expense.csv','a',encoding='utf-8',newline='') as f:
			fw = csv.writer(f)
			data = [details,rate,quantity,discount,amount,now,transactionID]
			fw.writerow(data)
		E1.focus()
		update_table()
	except Exception as e:
		print("ERROR", e)
		messagebox.showerror("ERROR","Please enter again.")
		#messagebox.showwarning("ERROR","Please enter again.")
		#messagebox.showinfo("ERROR","Please enter again.")
		v_details.set('')
		v_rate.set('')
		v_quantity.set('')
		v_discount.set('')
		E1.focus()

GUI.bind('<Return>',Save)

FONT1 = (None,15)

center_img = PhotoImage(file='Images/list-icon.png')
logo = ttk.Label(F1,image=center_img)
logo.pack()

# ---Text 1---
L = ttk.Label(F1,text='Details',font=FONT1).pack()
v_details = StringVar()
E1 = ttk.Entry(F1,textvariable=v_details,font=FONT1)
E1.pack()
# ------------

# ---Text 2---
L = ttk.Label(F1,text='Rate',font=FONT1).pack()
v_rate = StringVar()
E2 = ttk.Entry(F1,textvariable=v_rate,font=FONT1)
E2.pack()
# ------------

# ---Text 3---
L = ttk.Label(F1,text='Quantity',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
# ------------

# ---Text 4---
L = ttk.Label(F1,text='Discount',font=FONT1).pack()
v_discount = StringVar()
E4 = ttk.Entry(F1,textvariable=v_discount,font=FONT1)
E4.pack()
# ------------

submit_icon = PhotoImage(file='Images/save-icon.png')

B1 = ttk.Button(F1,text=f'{"Submit": >{5}}',command=Save,image=submit_icon,compound='left')
B1.pack(padx=0,pady=30)

v_result = StringVar()
#v_result.set("-----------------------------------")
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground="green")
result.pack(pady=20)

###########################Tab 2###############################

rs = []

def read_csv():
	with open('Expense.csv', newline='', encoding='utf-8') as f:
		fr = csv.reader(f) #fr = file reader
		data = list(fr)
	return data
		#print(list(fr))
		# print(data)
		# print('-----------')
		# print(data[0][0])
		# for d in data:
		# 	print(d[0])

		# for a,b,c,d,e,f in data:
		# 	print(c)

#rs = read_csv()
#print(rs)

# read_csv()
# print(rs)
L = ttk.Label(T2,text='Responses',font=FONT1).pack(pady=20)

header = ['Details','Rate','Quantity','Discount','Total','Timestamp','Transaction ID']
result_table = ttk.Treeview(T2, columns=header, show='headings',height=10)
result_table.pack()

# for i in range(len(header)):
# 	result_table.heading(header[i], text=header[i])

for h in header:
	result_table.heading(h,text=h)

headerwidth = [150,90,170,170,110,190,150]

for h,w in zip(header, headerwidth):
	result_table.column(h, width=w)

alltransaction = {}

def UpdateCSV():
	with open('Expense.csv', 'w', newline='', encoding='utf-8') as f:
		fw = csv.writer(f)
		# change alltransaction to list
		data = list(alltransaction.values())
		fw.writerows(data) # multiple line from nested list [[],[],[]]
		print("Table was updated")
		update_table()

def DeleteRecord(event=None):
	check = messagebox.askyesno('Conferm Delete?', 'Do you want to delete?')
	print('Yes/No:',check)

	if check == True:
		print('Delete')
		select = result_table.selection()
		#print(select)
		data = result_table.item(select)
		data = data['values']
		transactionID = data[-1]
		#print(transactionID)
		#print(type(transactionID))
		del alltransaction[str(transactionID)]
		#print(alltransaction)
		UpdateCSV()
		update_table()
	else:
		print("Cancel")

BDelete = ttk.Button(T2,text='Delete',command=DeleteRecord)
BDelete.place(x=50,y=550)

result_table.bind('<Delete>', DeleteRecord)

def update_table():
	result_table.delete(*result_table.get_children())
	# for c in result_table.get_children():
	# 	result_table.delete(c)
	try:
		data = read_csv()
		for d in data:
			# create transaction data
			alltransaction[d[-1]] = d
			result_table.insert('', 0, value=d)
		print(alltransaction)
	except:
		print("No file")

################Right click##################

def EditRecord():
	POPUP = Toplevel()
	POPUP.title('Edit Record')
	#POPUP.geometry('500x500')

	w = 500
	h = 500

	ws = POPUP.winfo_screenwidth() #screen width
	hs = POPUP.winfo_screenheight() #screen height


	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

	# ---Text 1---
	L = ttk.Label(POPUP,text='Details',font=FONT1).pack()
	v_details = StringVar()
	E1 = ttk.Entry(POPUP,textvariable=v_details,font=FONT1)
	E1.pack()
	# ------------

	# ---Text 2---
	L = ttk.Label(POPUP,text='Rate',font=FONT1).pack()
	v_rate = StringVar()
	E2 = ttk.Entry(POPUP,textvariable=v_rate,font=FONT1)
	E2.pack()
	# ------------

	# ---Text 3---
	L = ttk.Label(POPUP,text='Quantity',font=FONT1).pack()
	v_quantity = StringVar()
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
	E3.pack()
	# ------------

	# ---Text 4---
	L = ttk.Label(POPUP,text='Discount',font=FONT1).pack()
	v_discount = StringVar()
	E4 = ttk.Entry(POPUP,textvariable=v_discount,font=FONT1)
	E4.pack()
	# ------------

	def Edit():
		print(transactionID)
		print(alltransaction)
		olddata = alltransaction[str(transactionID)]
		print('OLD:', olddata)
		v1 = v_details.get()
		v2 = float(v_rate.get())
		v3 = float(v_quantity.get())
		v4 = float(v_discount.get())
		amount = v2 * v3 - v4
		newdata = [v1, v2, v3, v4, amount, olddata[-2], olddata[-1]]
		alltransaction[str(transactionID)] = newdata
		UpdateCSV()
		update_table()

		POPUP.destroy()

	submit_icon = PhotoImage(file='Images/save-icon.png')

	B1 = ttk.Button(POPUP,text=f'{"Submit": >{5}}',command=Edit,image=submit_icon,compound='left')
	B1.pack(padx=0,pady=30)

	

	# get data in selected record
	select = result_table.selection()
	print(select)
	data = result_table.item(select)
	data = data['values']
	print(data)
	transactionID = data[-1]

	v_details.set(data[0])
	v_rate.set(data[1])
	v_quantity.set(data[2])
	v_discount.set(data[3])

	POPUP.mainloop()

rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit', command=EditRecord)
rightclick.add_command(label='Delete', command=DeleteRecord)

def menupopup(event):
	#print(event.x_root, event.y_root)
	rightclick.post(event.x_root, event.y_root)

GUI.bind('<Button-3>', menupopup)

update_table()


GUI.mainloop()
