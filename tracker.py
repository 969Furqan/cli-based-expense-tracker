from ast import List
from ctypes import ArgumentError
from datetime import date
from logging import raiseExceptions
from typing import Tuple

expenses = Tuple[int, str, int, date]

class tracker:
    def __init__(self):

        self.table: List[expenses] = []
        self.count = 0
    
    def addexpense(self, description:str, amount:int):
        if amount < 0:
            raise ValueError("negative amount not possible")
        else:
            self.count += 1
            addDate = date.today()
            newExpense: expenses = [self.count, description, amount, addDate]
            self.table.append(newExpense)

    def updateExpense(self, id:int, description:str = None, amount:int = -1):
        for exp in self.table:
            if exp[0] == id:
                if description is None and amount == -1:
                    raise TypeError("no argument passed to update") 
                elif description is not None and amount == -1:
                    newEntry: expenses = [id, description, exp[2], exp[3]]
                    self.table.remove(exp)
                    break
                elif description is  None and amount != -1:
                    newEntry: expenses = [id, exp[1], amount, exp[3]]
                    self.table.remove(exp)
                    break
                elif description is not None and amount != -1:
                    newEntry: expenses = [id, description, amount, exp[3]]
                    self.table.remove(exp)
                    break;
        self.table.append(newEntry)

    def deleteExpense(self, id:int):
        for expense in self.table:
            if expense[0] == id:
                print(expense)
                self.table.remove(expense)
                break

    def listExpenses(self):
        if self.table == []:
            raise ValueError("expense list is empty")
        else:
            for expense in self.table:
                print(f"id: {expense[0]}, description: {expense[1]}, amount{expense[2]}, date added{expense[3]}")

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
        
                



if __name__ == "__main__":
    
    t = tracker()

    t.addexpense("eggs", 500)
    t.addexpense("bread", 200)
    t.addexpense("chicken", 1200)
    print("\nbefore delete is run\n")
    t.deleteExpense(2)
    print("\nafter delete is run\n")
    t.expenseSummary("september")
    