import graph
import tkinter
from tkinter import *
from tkinter import ttk
import sqlite3 as db

from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime


def init():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    create table if not exists expenses (
        date string,
        name string,
        title string,
        expense number
        )
    '''

    query2 = '''
        create table if not exists income (
            date string,
            name string,
            title string,
            expense number
            )
        '''
    curr.execute(query)
    curr.execute(query2)
    connectionObjn.commit()


# function to submit the data to the database by user
def submitexpense():
    values = [dateEntry.get(), Name.get(), Title.get(), Expense.get()]
    print(values)
    Etable.insert('', 'end', values=values)

    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    INSERT INTO expenses VALUES 
    (?, ?, ?, ?)
    '''

    if Title.get() is None or Expense.get() == 0 or None:
        messagebox.showinfo("Alert", "Please input data")
    else:
        curr.execute(query, (dateEntry.get(), Name.get(),
                     Title.get(), Expense.get()))
        connectionObjn.commit()

    # dateEntry.get(), Name.get(),
    Title.set('')
    Expense.set(0)


# Showing only the income amount details
def incomeOnly(my_game, rows):
    print("inside income only")
    for row in my_game.get_children():
        my_game.delete(row)
    for i in rows:
        val = ()
        if i[1] == "Income":
            for j in i:
                val = val + (j,)
            my_game.insert(parent='', index='end', text='', values=val)


# Showing only the expense amount details
def expenseOnly(my_game, rows):
    print("inside expense only")
    for row in my_game.get_children():
        my_game.delete(row)
    for i in rows:
        val = ()
        if i[1] == "Expense":
            for j in i:
                val = val + (j,)
            my_game.insert(parent='', index='end', text='', values=val)


# function to view all the data of income and expense
def viewexpense(pastPresent):
    print("This month : = " + '%02d' % datetime.now().month)

    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    if pastPresent == "Past":
        monthNow = int(datetime.now().month) - 1
        query = f'''
             select * from expenses where strftime('%m', date) = '{'%02d' % monthNow}'
            '''

    else:
        query = f'''
                     select * from expenses where strftime('%m', date) = '{'%02d' % datetime.now().month}'
                    '''
    total = '''
                select sum(expense) from expenses
                '''

    curr.execute(query)
    rows = curr.fetchall()
    curr.execute(total)
    amount = curr.fetchall()[0]
    # print(rows)
    # print(amount)

    win = Toplevel()
    win.geometry('400x500')
    win.title('Income/Expense Data')

    game_frame = Frame(win)
    # game_frame.winfo_geometry('430x500')
    game_frame.pack()
    my_game = ttk.Treeview(game_frame, height=15)

    my_game['columns'] = ('date', 'type', 'title', 'amount')

    my_game.column("#0", width=0, stretch=NO)
    my_game.column("date", anchor=CENTER, width=90)
    my_game.column("type", anchor=CENTER, width=90)
    my_game.column("title", anchor=CENTER, width=90)
    my_game.column("amount", anchor=CENTER, width=90)

    my_game.heading("#0", text="", anchor=CENTER)
    my_game.heading("date", text="Date", anchor=CENTER)
    my_game.heading("type", text="Type", anchor=CENTER)
    my_game.heading("title", text="Title", anchor=CENTER)
    my_game.heading("amount", text="Amount", anchor=CENTER)

    def allValue():
        for row in my_game.get_children():
            my_game.delete(row)
        for i in rows:
            val = ()
            for j in i:
                val = val + (j,)
            my_game.insert(parent='', index='end', text='', values=val)

    allValue()

    my_game.pack()

    if pastPresent == "Past":
        monthNow = int(datetime.now().month) - 1

        query = f'''SELECT name FROM expenses where strftime('%m', date) = '{'%02d' % monthNow}'
                '''
        curr.execute(query)  # execute a simple SQL select query
        type = curr.fetchall()  # get all the results from the above query

        query2 = f'''SELECT expense FROM expenses where strftime('%m', date) = '{'%02d' % monthNow}'
                '''
        curr.execute(query2)
        money = curr.fetchall()
    else:
        # execute a simple SQL select query
        curr.execute("SELECT name FROM expenses ")
        type = curr.fetchall()  # get all the results from the above query

        curr.execute("SELECT expense FROM expenses")
        money = curr.fetchall()

    type1 = []
    money1 = []

    for y in type:
        type1.append(y[0])
    for z in money:
        money1.append(z[0])

    moneyIncome = 0
    moneyExpense = 0

    for x in range(len(type1)):
        if type1[x] == 'Expense':
            moneyExpense += money1[x]
        else:
            moneyIncome += money1[x]

    print(moneyExpense)
    print(moneyIncome)

    l = Label(win, text='Total Income = ' +
              str(moneyIncome), font=('arial', 12))
    l.pack()
    # l.grid(row=7, column=0, padx=5, pady=5)

    l2 = Label(win, text='Total Expense = ' +
               str(moneyExpense), font=('arial', 12))
    l2.pack()
    # l2.grid(row=8, column=0, padx=5, pady=5)

    buttonExpenseOnly = Button(
        win, text='Expense Only', command=lambda: expenseOnly(my_game, rows))
    buttonExpenseOnly.pack()
    buttonExpenseOnly.place(relx=0.3, rely=0.8, anchor=CENTER)

    buttonIncomeOnly = Button(win, text='Income Only',
                              command=lambda: incomeOnly(my_game, rows))
    buttonIncomeOnly.pack()
    buttonIncomeOnly.place(relx=0.7, rely=0.8, anchor=CENTER)

    buttonAll = Button(win, text='Income/Expense', command=allValue)
    buttonAll.pack()
    buttonAll.place(relx=0.5, rely=0.9, anchor=CENTER)


#  Asking the user for the chart type
def chartType():
    pieChart = graph.graphChart()
    win = Toplevel()
    win.geometry('300x100')
    win.title('PIE CHART')
    message = "Select the chart"
    Label(win, text=message).pack()
    button1 = Button(win, text='Expense', command=pieChart.viewPieExpense)
    button1.pack(side=tkinter.LEFT)
    button1.place(relx=0.3, rely=0.5, anchor=CENTER)

    button2 = Button(win, text='Income', command=pieChart.viewPieIncome)
    button2.pack(side=tkinter.RIGHT)
    button2.place(relx=0.7, rely=0.5, anchor=CENTER)


# comapring with the past vs present income/expense
def compareChart():
    piechart2 = graph.graphChart()
    win = Toplevel()
    win.geometry('400x100')
    win.title('PIE CHART')
    message = "Select chart to compare past month vs current month"
    Label(win, text=message).pack()
    button1 = Button(win, text='Expense', command=piechart2.compareExpense)
    button1.pack(side=tkinter.LEFT)
    button1.place(relx=0.3, rely=0.5, anchor=CENTER)

    button2 = Button(win, text='Income', command=piechart2.compareIncome)
    button2.pack(side=tkinter.RIGHT)
    button2.place(relx=0.7, rely=0.5, anchor=CENTER)


init()
root = Tk()
root.title("Income/Expense Calculator")
root.geometry('800x600')

dateLabel = Label(root, text="Date", font=('arial', 15, 'bold'),
                  bg="DodgerBlue2", fg="white", width=12)
dateLabel.grid(row=0, column=0, padx=7, pady=7)

dateEntry = DateEntry(root, width=12, font=('arial', 15, 'bold'))
dateEntry.grid(row=0, column=1, padx=7, pady=7)

Name = StringVar()
nameLabel = Label(root, text="Type", font=('arial', 15, 'bold'),
                  bg="DodgerBlue2", fg="white", width=12)
nameLabel.grid(row=1, column=0, padx=7, pady=7)

# NameEntry = Entry(root, textvariable=Name, font=('arial', 15, 'bold'))
# Dropdown menu options
options = [
    "Expense",
    "Income",
]

# datatype of menu text
Name = StringVar()

# initial menu text
Name.set("Expense")

# Create Dropdown menu
NameEntry = OptionMenu(root, Name, *options)
# drop.pack()
# NameEntry.grid(row=1, column=1, padx=7, pady=7)
NameEntry.grid(row=1, column=1, padx=7, pady=7)

Title = StringVar()
titleLabel = Label(root, text="Title", font=(
    'arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
titleLabel.grid(row=2, column=0, padx=7, pady=7)

titleEntry = Entry(root, textvariable=Title, font=('arial', 15, 'bold'))
titleEntry.grid(row=2, column=1, padx=7, pady=7)

Expense = IntVar()
expenseLabel = Label(root, text="Amount", font=(
    'arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
expenseLabel.grid(row=3, column=0, padx=7, pady=7)

expenseEntry = Entry(root, textvariable=Expense, font=('arial', 15, 'bold'))
expenseEntry.grid(row=3, column=1, padx=7, pady=7)

submitbtn = Button(root, command=submitexpense, text="Submit", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white",
                   width=12)
submitbtn.grid(row=4, column=0, padx=13, pady=13)

viewtn = Button(root, command=lambda: viewexpense(""), text="View data", font=('arial', 15, 'bold'), bg="DodgerBlue2",
                fg="white", width=12)
viewtn.grid(row=4, column=1, padx=13, pady=13)

viewctn = Button(root, command=chartType, text="View chart", font=('arial', 15, 'bold'), bg="DodgerBlue2",
                 fg="white", width=12)
viewctn.grid(row=4, column=2, padx=13, pady=13)

# all saved expenses--------------
Elist = ['Date', 'Type', 'Title', 'Amount']
Etable = ttk.Treeview(root, column=Elist, show='headings', height=7)
for c in Elist:
    Etable.heading(c, text=c.title())
Etable.grid(row=5, column=0, padx=7, pady=7, columnspan=3)

expenseHistory = Button(root, command=lambda: viewexpense("Past"), text="Past Month", font=('arial', 15, 'bold'),
                        bg="DodgerBlue2",
                        fg="white", width=12)
expenseHistory.grid(row=6, column=0)

compareChart = Button(root, command=compareChart, text="Compare Chart", font=('arial', 15, 'bold'),
                      bg="DodgerBlue2",
                      fg="white", width=12)
compareChart.grid(row=6, column=1)

mainloop()
