#! /opt/miniconda3/bin/python3
'''
tracker is an app that maintains a list of personal
financial transactions.

It uses Object Relational Mappings (ORM)
to abstract out the database operations from the
UI/UX code.

The ORM, Category, will map SQL rows with the schema
  (rowid, category, description)
to Python Dictionaries as follows:

(5,'rent','monthly rent payments') <-->

{rowid:5,
 category:'rent',
 description:'monthly rent payments'
 }

Likewise, the ORM, Transaction will mirror the database with
columns:
amount, category, date (yyyymmdd), description


In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/tracker.db

Note the actual implementation of the ORM is hidden and so it
could be replaced with PostgreSQL or Pandas or straight python lists

'''

from transactions import Transaction
from category import Category

TRANSACTION = Transaction('tracker.db')
CATEGORY = Category('tracker.db')

# here is the menu for the tracker app

MENU = '''
0. quit
1. show categories
2. add category
3. modify category
4. show transactions
5. add transaction
6. delete transaction
7. summarize transactions by date
8. summarize transactions by month
9. summarize transactions by year
10. summarize transactions by category
11. print this menu
'''

def process_choice(choice):
    '''prompts user for their menu choice'''
    transaction = TRANSACTION
    category = CATEGORY
    if choice=='1':
        cats = category.select_all()
        print_categories(cats)
    elif choice=='2':
        name = input("category name: ")
        desc = input("category description: ")
        cat = {'name':name, 'desc':desc}
        category.add(cat)
    elif choice=='3':
        print("modifying category")
        rowid = int(input("rowid: "))
        name = input("new category name: ")
        desc = input("new category description: ")
        cat = {'name':name, 'desc':desc}
        category.update(rowid,cat)
    elif choice=='4':
        print_transactions(transaction.show_transactions())
    elif choice == '5':
        amount = int(input("amount: "))
        ctgry = input("category: ")
        date = input("date: ")
        description = input("description: ")
        tran = {'amount':amount, 'category':ctgry,
            'date':date, 'description':description}
        transaction.add(tran)
        cat = {'name':ctgry, 'desc':description}
        category.add(cat)
    elif choice == '6':
        item_num = input("item_num: ")
        transaction.delete(item_num)
        print('DELETE CORRELATING CATEGORY ')
        cats = category.select_all()
        print_categories(cats)
        row = input("category rowid: ")
        category.delete(row)
    elif choice == '7':
        bgn = input("start date (yyyymmdd): ")
        end = input("end date (yyyymmdd): ")
        print_transactions(transaction.print_sum_date(bgn, end))
        total = transaction.date_total(bgn, end)
        print("%-10s %-10d"%("Total:", total))
    elif choice == '8':
        month = input("month (mm): ")
        print_transactions(transaction.print_sum_month(month))
        total = transaction.month_total(month)
        print("%-10s %-10d"%("Total:", total))
    elif choice == '9':
        year = input("year (yyyy): ")
        print_transactions(transaction.print_sum_year(year))
        total = transaction.year_total(year)
        print("%-10s %-10d"%("Total:", total))
    elif choice == '10':
        sum_cat = input("category: ")
        print_transactions(transaction.print_sum_cat(sum_cat))
        total = transaction.cat_total(sum_cat)
        print("%-10s %-10d"%("Total:", total))
    elif choice == '11':
        print(MENU)
    choice = input("> ")
    return process_choice(choice)

def toplevel():
    ''' handle the user's choice
        read the command args and process them'''
    print(MENU)
    choice = input("> ")
    while choice !='0':
        choice = process_choice(choice)
    print('bye')

# here are some helper functions
def print_transactions(items):
    ''' print the transactions '''
    if len(items)==0:
        print('no transactions to print')
        return
    print('\n')
    print("%-10s %-10s %-10s %-10s %-30s"%(
        'item_num','amount','category','date','description'))
    print('-'*60)
    for item in items:
        values = tuple(item.values())
        print("%-10d %-10d %-10s %-10d %-30s"%values)

def print_category(cat):
    '''prints data for each category'''
    print("%-3d %-10s %-30s"%(cat['rowid'],cat['name'],cat['desc']))

def print_categories(cats):
    '''prints each category in categories table'''
    if len(cats)==0:
        print('no categories to print')
        return
    print("%-3s %-10s %-30s"%("id","name","description"))
    print('-'*45)
    for cat in cats:
        print_category(cat)

# here is the main call!
toplevel()
