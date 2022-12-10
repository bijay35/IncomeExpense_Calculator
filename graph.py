# Class for the pie chart graph
import sqlite3 as db
from datetime import datetime

import plotly.graph_objects as go
from PIL import Image as PImage


class graphChart:
    # Function to show the chart
    def viewPieExpense(self):
        connectionObjn = db.connect("expenseTracker.db")
        curr = connectionObjn.cursor()
        curr.execute("SELECT name FROM expenses")  # execute a simple SQL select query
        nameExpense = curr.fetchall()  # get all the results from the above query

        curr.execute("SELECT title FROM expenses")  # execute a simple SQL select query
        jobsExpense = curr.fetchall()  # get all the results from the above query

        curr.execute("SELECT expense FROM expenses")
        moneyExpense = curr.fetchall()

        labelExpense = []
        pointsExpense = []
        name2Expense = []
        label_expense = []
        points_expense = []

        for x in jobsExpense:
            labelExpense.append(x[0])
        for y in moneyExpense:
            pointsExpense.append(y[0])
        for z in nameExpense:
            name2Expense.append(z[0])

        for x in range(len(name2Expense)):
            if name2Expense[x] == 'Expense':
                label_expense.append(labelExpense[x])
                points_expense.append(pointsExpense[x])

        # plt.pie(points_expense, labels=label_expense)
        # plt.savefig("Expense.png")

        fig = go.Figure(data=[go.Pie(labels=label_expense, values=points_expense, hole=.3)])
        fig.write_image("./imageExpense.png")
        # fig.show()

        img = PImage.open("./imageExpense.png")
        img.show()

    # function to show the chart for the income
    def viewPieIncome(self):
        connectionObjn = db.connect("expenseTracker.db")
        curr = connectionObjn.cursor()
        curr.execute("SELECT name FROM expenses")  # execute a simple SQL select query
        name = curr.fetchall()  # get all the results from the above query

        curr.execute("SELECT title FROM expenses")  # execute a simple SQL select query
        jobs = curr.fetchall()  # get all the results from the above query

        curr.execute("SELECT expense FROM expenses")
        money = curr.fetchall()

        label = []
        points = []
        name2 = []
        label_income = []
        points_income = []

        for x in jobs:
            label.append(x[0])
        for y in money:
            points.append(y[0])
        for z in name:
            name2.append(z[0])

        for x in range(len(name2)):
            if name2[x] == 'Income':
                label_income.append(label[x])
                points_income.append(points[x])

        fig = go.Figure(data=[go.Pie(labels=label_income, values=points_income, hole=.3)])
        fig.write_image("./imageIncome.png")
        # fig.show()

        img = PImage.open("./imageIncome.png")
        img.show()

    # function to compare past and present income/expense
    def compareIncome(self):
        monthNow = int(datetime.now().month) - 1
        connectionObjn = db.connect("expenseTracker.db")
        curr = connectionObjn.cursor()

        # /*----------------------- Past data ---------------------------*/
        query_income_past = f'''SELECT name FROM expenses where strftime('%m', date) = '{'%02d' % monthNow}'
                        '''
        curr.execute(query_income_past)  # execute a simple SQL select query
        type_income_past = curr.fetchall()  # get all the results from the above query

        query2_income_past = f'''SELECT expense FROM expenses where strftime('%m', date) = '{'%02d' % monthNow}'
                        '''
        curr.execute(query2_income_past)
        money_income_past = curr.fetchall()
        # /* ----------------------------------------------------------------*/

        # /*-------------------------- Present data --------------------*/
        query_income_present = f'''SELECT name FROM expenses where strftime('%m', date) = '{'%02d' % datetime.now().month}' 
                                '''
        curr.execute(query_income_present)  # execute a simple SQL select query
        type_income_present = curr.fetchall()  # get all the results from the above query

        query2_income_present = f'''SELECT expense FROM expenses where strftime('%m', date) = '{'%02d' % datetime.now().month}'
                                '''
        curr.execute(query2_income_present)
        money_income_present = curr.fetchall()
        # /*---------------------------------------------------------------------------*/

        type_income_past_2 = []
        type_income_present_2 = []
        money_income_past_2 = []
        money_income_present_2 = []
        income_past = 0
        income_present = 0
        expense_past = 0
        expense_present = 0

        for x in type_income_past:
            type_income_past_2.append(x[0])

        for y in type_income_present:
            type_income_present_2.append(y[0])

        for x in money_income_past:
            money_income_past_2.append(x[0])
        for y in money_income_present:
            money_income_present_2.append(y[0])

        print(type_income_past_2)
        print(type_income_present_2)

        for x in range(len(type_income_past_2)):
            if type_income_past_2[x] == "Income":
                income_past = income_past + money_income_past_2[x]
            else:
                expense_past = expense_past + money_income_past_2[x]

        for y in range(len(type_income_present_2)):
            if type_income_present_2[y] == "Income":
                income_present = income_present + money_income_present_2[y]
            else:
                expense_present = expense_present + money_income_present_2[y]

        print(income_past)
        print(expense_past)

        print(income_present)
        print(expense_present)

        label_income = ["Past Month", "This month"]
        points_income = [income_past, income_present]

        fig = go.Figure(data=[go.Pie(labels=label_income, values=points_income, hole=.3)])
        fig.write_image("./imageIncome.png")
        # fig.show()

        img = PImage.open("./imageIncome.png")
        img.show()

    def compareExpense(self):
        monthNow = int(datetime.now().month) - 1
        connectionObjn = db.connect("expenseTracker.db")
        curr = connectionObjn.cursor()

        # /*----------------------- Past data ---------------------------*/
        query_income_past = f'''SELECT name FROM expenses where strftime('%m', date) = '{'%02d' % monthNow}'
                        '''
        curr.execute(query_income_past)  # execute a simple SQL select query
        type_income_past = curr.fetchall()  # get all the results from the above query

        query2_income_past = f'''SELECT expense FROM expenses where strftime('%m', date) = '{'%02d' % monthNow}'
                        '''
        curr.execute(query2_income_past)
        money_income_past = curr.fetchall()
        # /* ----------------------------------------------------------------*/

        # /*-------------------------- Present data --------------------*/
        query_income_present = f'''SELECT name FROM expenses where strftime('%m', date) = '{'%02d' % datetime.now().month}' 
                                '''
        curr.execute(query_income_present)  # execute a simple SQL select query
        type_income_present = curr.fetchall()  # get all the results from the above query

        query2_income_present = f'''SELECT expense FROM expenses where strftime('%m', date) = '{'%02d' % datetime.now().month}'
                                '''
        curr.execute(query2_income_present)
        money_income_present = curr.fetchall()
        # /*---------------------------------------------------------------------------*/

        type_income_past_2 = []
        type_income_present_2 = []
        money_income_past_2 = []
        money_income_present_2 = []
        income_past = 0
        income_present = 0
        expense_past = 0
        expense_present = 0

        for x in type_income_past:
            type_income_past_2.append(x[0])

        for y in type_income_present:
            type_income_present_2.append(y[0])

        for x in money_income_past:
            money_income_past_2.append(x[0])
        for y in money_income_present:
            money_income_present_2.append(y[0])

        print(type_income_past_2)
        print(type_income_present_2)

        for x in range(len(type_income_past_2)):
            if type_income_past_2[x] == "Income":
                income_past = income_past + money_income_past_2[x]
            else:
                expense_past = expense_past + money_income_past_2[x]

        for y in range(len(type_income_present_2)):
            if type_income_present_2[y] == "Income":
                income_present = income_present + money_income_present_2[y]
            else:
                expense_present = expense_present + money_income_present_2[y]

        print(income_past)
        print(expense_past)

        print(income_present)
        print(expense_present)

        label_income = ["Past Month", "This month"]
        points_income = [expense_past, expense_present]

        fig = go.Figure(data=[go.Pie(labels=label_income, values=points_income, hole=.3)])
        fig.write_image("./imageCompareExpense.png")
        # fig.show()

        img = PImage.open("./imageCompareExpense.png")
        img.show()