'''
transactions.py is a Object Relational Mapping to the transactions table

The ORM will work map SQL rows with the schema
    (item_num, amount, category, date, description)
to Python Dictionaries.

This app will store the data in a SQLite database ~/tracker.db

'''

import sqlite3
import os

def to_dict(tran):
    ''' t is a tuple (rowid, amount, category, date, description)'''
    transactions = {'rowid':tran[0], 'amount':tran[1], 'category':tran[2], 'date':tran[3], 'description':tran[4]}
    return transactions

def to_transaction_dict_list(tran_tuples):
    ''' convert a list of category tuples into a list of dictionaries'''
    return [to_dict(tran) for tran in tran_tuples]

class Transaction():
    ''' Transaction represents a table of transactions'''

    #Class Constructor; initialization
    def __init__(self, dbFile):
        con= sqlite3.connect(dbFile)
        cur = con.cursor() 
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions
            (amount int, category text, date int, description text)''')
        con.commit()
        con.close()
        self.dBase = dbFile


    #Menu opt 4; show transactions
    def show_transactions(self):
        '''shows all transactions'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute("SELECT rowid,* from transactions")
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_transaction_dict_list(tuples)


    #Menu opt 5; add transaction
    def add_transactions(self, transaction):
        '''adds a new transaction
        this returns the item_num of the inserted element'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute("INSERT INTO transactions VALUES(?,?,?,?)",
            (transaction['amount'],transaction['category'],
            transaction['date'],transaction['description']))
        con.commit()
        cur.execute("SELECT last_insert_rowid()")
        last_item_num = cur.fetchone()
        con.commit()
        con.close()
        return last_item_num[0]


    #Menu opt 6; delete transaction
    def del_transactions(self, itemnum):
        '''deletes a transaction'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        del_trans = cur.execute('''SELECT * FROM transactions WHERE rowid=(?)''',(itemnum,)).fetchone()
        con.commit()
        del_cat = del_trans[1]
        del_desc = del_trans[3]
        cur.execute('''DELETE FROM categories WHERE name=(?) AND desc=(?)''',(del_cat, del_desc,))
        cur.execute('''DELETE FROM transactions WHERE rowid=(?) ''',(itemnum,))
        con.commit()
        con.close()
        return
    

    #Menu opt 7; summarize transactions by date
    def print_sum_date(self, bgn, end):
        '''shows transactions between provided dates (inclusive)'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT rowid,* FROM transactions
            WHERE date>=(?) AND date<=(?)''', (bgn,end,))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_transaction_dict_list(tuples)

    def date_total(self, bgn, end):
        '''calculates total spent between provided dates (inclusive)'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT SUM(amount) FROM transactions
            WHERE date>=(?) AND date<=(?)''', (bgn,end,))
        sum_tup = cur.fetchone()
        con.commit()
        con.close()
        return sum_tup[0]


    #Menu opt 8; summarize transactions by month
    def print_sum_month(self, month):
        '''shows transactions from provided month'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        # cur.execute('''SELECT *,SUBSTRING(date, 5, 2) AS month FROM transactions
        #     GROUP BY month''')
        cur.execute('''SELECT rowid,* FROM transactions 
            WHERE CAST(SUBSTRING(date, 5, 2) AS int)=(?)''', (month,))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_transaction_dict_list(tuples)
        
    def month_total(self, month):
        '''calculates total from provided month'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT SUM(amount) FROM transactions
            WHERE CAST(SUBSTRING(date, 5, 2) AS int)=(?)''', (month,))
        sum_tup = cur.fetchone()
        con.commit()
        con.close()
        return sum_tup[0]


    #Menu opt 9; summarize transactions by year
    def print_sum_year(self, year):
        '''shows transactions from provided year'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT rowid,* FROM transactions 
            WHERE CAST(SUBSTRING(date, 1, 4) AS int)=(?)''', (year,))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_transaction_dict_list(tuples)

    def year_total(self, year):
        '''calculates total from provided year'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT SUM(amount) FROM transactions
            WHERE CAST(SUBSTRING(date, 1, 4) AS int)=(?)''', (year,))
        sum_tup = cur.fetchone()
        con.commit()
        con.close()
        return sum_tup[0]        


    #Menu opt 10; summarize transactions by category
    def print_sum_cat(self,cat):
        '''shows transactions from provided category'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT rowid,* FROM transactions
            WHERE category=(?)''',(cat,))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_transaction_dict_list(tuples)

    def cat_total(self, cat):
        '''calculates total from provided category'''
        con= sqlite3.connect(self.dBase)
        cur = con.cursor()
        cur.execute('''SELECT SUM(amount) FROM transactions
            WHERE category=(?)''', (cat,))
        sum_tup = cur.fetchone()
        con.commit()
        con.close()
        return sum_tup[0]

