from ast import List
from datetime import date
import json
from logging import raiseExceptions
from typing import Tuple
import argparse

expenses = Tuple[int, str, int, date]

class tracker:
    def __init__(self, fileName):

        self.table: List[expenses] = []
        self.count = 0
        self.filename = fileName
        self.loadExpense()
    
    def addexpense(self, description:str, amount:int):
        if amount < 0:
            raise ValueError("negative amount not possible")
        else:
            self.count += 1
            addDate = date.today()
            newExpense: expenses = [self.count, description, amount, addDate]
            self.table.append(newExpense)
            self.storeExpense()

    def updateExpense(self, id:int, description:str = None, amount = None):
        newEntry = None
        for exp in self.table:
            if exp[0] == id:
                if description is not None and amount is not None:
                    newEntry: expenses = [id, description, amount, exp[3]]
                    self.deleteExpense(id)
                
                elif description is  None and amount is not None:
                    newEntry: expenses = [id, exp[1], amount, exp[3]]
                    self.deleteExpense(id)
                elif description is not None and amount is None:
                    newEntry: expenses = [id, description, exp[2], exp[3]]
                    self.deleteExpense(id)
        self.table.append(newEntry)
        self.storeExpense()

    def deleteExpense(self, id:int):
        for expense in self.table:
            if expense[0] == id:
                self.table.remove(expense)
                break
        self.storeExpense()

    def listExpenses(self):
        
        for expense in self.table:
            print(f"id: {expense[0]}\tdescription:{expense[1]}\tamount:{expense[2]}\tdate added:{expense[3]}")

    def expenseSummary(self, month:str = None):
        total = 0
        if month is not None: 
            templist: List[expenses] = []
            for expenses in self.table:
                x = expenses[3].strftime("%B")
                if(x.capitalize() == month.capitalize()):
                    templist.append(expenses)
            
            for expense in templist:
                    total = total + expense[2]

            print(F"The total expenses for the month {x} is {total}$")
        elif month is None:
            for expense in self.table:
                    total = total + expense[2]

            print(F"The total is {total}$")

    def storeExpense(self):
        data = [
            {
                "id":item[0],
                "name":item[1],
                "amount":item[2],
                "date":item[3].isoformat()
            } for item in self.table
        ]
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def loadExpense(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.table = [
                    (
                        item["id"],
                        item["name"],
                        item["amount"],
                        date.fromisoformat(item["date"])
                        
                    )
                    for item in data
                ]
                if self.table:
                    self.count = max(expense[0] for expense in self.table)
        except FileNotFoundError:
            print("file not found")
        
                



if __name__ == "__main__":

    parser = argparse.ArgumentParser("expense", description="An expense tracker application")
    subparser = parser.add_subparsers(dest = "command", required= True)
#
    add_expense = subparser.add_parser("add", help = "add expenses")
    add_expense.add_argument("name", type= str)
    add_expense.add_argument("amount", type= int)
#
    delete_expense = subparser.add_parser("delete", help = "delete an expense")
    delete_expense.add_argument("id", type = int)
#
    list_expense = subparser.add_parser("list", help= "list the expenses")
#
    update_expense = subparser.add_parser("update", help = "update an expense")
    update_expense.add_argument("id", type = int)
    update_expense.add_argument("--name", type = str)
    update_expense.add_argument("--amount", type = int)
#
#
    args = parser.parse_args()
    t = tracker("expenses.json")


    if args.command == "add":
        t.addexpense(args.name, args.amount)
    if args.command == "list":
        t.listExpenses()
    if args.command == "delete":
        t.deleteExpense(args.id)
    if args.command == "update":
        print (f"args are \n{args.id}\n{args.name}\n{args.amount}")
        if  args.name and args.amount:
            t.updateExpense(args.id, args.name, args.amount)
        elif args.name:
            t.updateExpense(args.id, description= args.name)
        elif args.amount:
            t.updateExpense(args.id, amount= args.amount)


    

    