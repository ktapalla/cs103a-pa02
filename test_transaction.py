'''
test_transaction runs unit and integration tests on the transaction module
'''

import pytest
from transactions import Transaction, to_transaction_dict

@pytest.fixture
def dbfile(tmpdir):
    ''' create a database file in a temporary file system '''
    return tmpdir.join('test_tracker.db')

@pytest.fixture
def empty_db(dbfile):
    ''' create an empty database '''
    db = Transaction(dbfile)
    yield db

@pytest.fixture
def small_db(empty_db):
    ''' create a small database, and tear it down later'''
    tran1 = {'amount':10,'category':'food','date':20100101,'description':'groceries'}
    tran2 = {'amount':20,'category':'ent','date':20100101,'description':'movie'}
    tran3 = {'amount':30,'category':'travel','date':20110601,'description':'uber'}
    tran4 = {'amount':40,'category':'food','date':20120101,'description':'dinner out'}
    tran5 = {'amount':50,'category':'ent','date':20110601,'description':'theme park'}
    tran6 = {'amount':60,'category':'travel','date':20120101,'description':'flight'}
    tran7 = {'amount':70,'category':'bills','date':20120601,'description':'monthly rent'}
    id1=empty_db.add(tran1)
    id2=empty_db.add(tran2)
    id3=empty_db.add(tran3)
    id4=empty_db.add(tran4)
    id5=empty_db.add(tran5)
    id6=empty_db.add(tran6)
    id7=empty_db.add(tran7)
    yield empty_db
    empty_db.delete(id7)
    empty_db.delete(id6)
    empty_db.delete(id5)
    empty_db.delete(id4)
    empty_db.delete(id3)
    empty_db.delete(id2)
    empty_db.delete(id1)

@pytest.fixture
def med_db(small_db):
    ''' create a database with 7 more elements than small_db'''
    tran8 = {'amount':80,'category':'travel','date':20110114,'description':'gas'}
    tran9 = {'amount':90,'category':'ent','date':20110406,'description':'movie'}
    tran10 = {'amount':100,'category':'travel','date':20110601,'description':'uber'}
    tran11 = {'amount':110,'category':'bills','date':20120601,'description':'power'}
    tran12 = {'amount':120,'category':'bills','date':20120601,'description':'water'}
    tran13 = {'amount':130,'category':'food','date':20120604,'description':'brunch'}
    tran14 = {'amount':140,'category':'bills','date':20130601,'description':'monthly rent'}
    id8=small_db.add(tran8)
    id9=small_db.add(tran9)
    id10=small_db.add(tran10)
    id11=small_db.add(tran11)
    id12=small_db.add(tran12)
    id13=small_db.add(tran13)
    id14=small_db.add(tran14)
    yield small_db
    small_db.delete(id14)
    small_db.delete(id13)
    small_db.delete(id12)
    small_db.delete(id11)
    small_db.delete(id10)
    small_db.delete(id9)
    small_db.delete(id8)

@pytest.mark.todo
@pytest.mark.print
@pytest.mark.simple
@pytest.mark.transaction
def test_to_transaction_dict():
    ''' testing the to_transaction_dict function '''
    a = to_transaction_dict((0, 100,'testcat', 20000101, 'testdesc'))
    assert a['rowid']==0
    assert a['amount']== 100
    assert a['category']=='testcat'
    assert a['date']== 20000101
    assert a['description']=='testdesc'
    assert len(a.keys())==5


@pytest.mark.print
@pytest.mark.small
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_select_one(small_db, med_db):
    ''' testing the select_one function'''
    sml = small_db.select_one(1)
    assert sml['rowid'] == 1
    assert sml['amount'] == 10
    assert sml['category'] == 'food'
    assert sml['date'] == 20100101
    assert sml['description'] == 'groceries'
    med = med_db.select_one(8)
    assert med['rowid'] == 8
    assert med['amount'] == 80
    assert med['category'] == 'travel'
    assert med['date'] == 20110114
    assert med['description'] == 'gas'


@pytest.mark.print
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_show_transactions(med_db):
    ''' testing the show_transactions function'''
    med = len(med_db.show_transactions())
    assert med == 14
    

@pytest.mark.add
@pytest.mark.data
@pytest.mark.simple
@pytest.mark.transaction
def test_add(med_db):
    ''' testing the add_transactions function
    add a transaction to db, then select it, then delete it'''
    tran0 = {'amount':100,
            'category':'test_add',
            'date':20220101,
            'description':'see if it works',
            }
    trans0 = med_db.show_transactions()
    rowid = med_db.add(tran0)
    trans1 = med_db.show_transactions()
    assert len(trans1) == len(trans0) + 1
    tran1 = med_db.select_one(rowid)
    assert tran1['amount']==tran0['amount']
    assert tran1['category']==tran0['category']
    assert tran1['date']==tran0['date']
    assert tran1['description']==tran0['description']

@pytest.mark.delete
@pytest.mark.data
@pytest.mark.simple
@pytest.mark.transaction
def test_delete(med_db):
    ''' testing the delete function
    add a transaction to db, delete it, and see that the size changes'''
    # first we get the initial table
    trans0 = med_db.show_transactions()

    # then we add this category to the table and get the new list of rows
    tran0 = {'amount':100,
            'category':'test_add',
            'date':20220101,
            'description':'see if it works',
            }
    rowid = med_db.add(tran0)
    trans1 = med_db.show_transactions()

    # now we delete the category and again get the new list of rows
    med_db.delete(rowid)
    trans2 = med_db.show_transactions()

    assert len(trans0)==len(trans2)
    assert len(trans2) == len(trans1)-1

@pytest.mark.print
@pytest.mark.date
@pytest.mark.cal
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_date_small(small_db):
    ''' testing the print_sum_date function with small_db'''
    test1 = small_db.print_sum_date(20100101, 20110601)
    test1_len = len(test1)
    assert test1_len == 4
    test2 = small_db.print_sum_date(20100101, 20120101)
    test2_len = len(test2)
    assert test2_len == 6
    test3 = small_db.print_sum_date(20100101, 20120601)
    test3_len = len(test3)
    assert test3_len == 7

@pytest.mark.print
@pytest.mark.date
@pytest.mark.cal
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_date_med(med_db):
    ''' testing the print_sum_date function with med_db'''
    test1 = med_db.print_sum_date(20100101, 20110601)
    test1_len = len(test1)
    assert test1_len == 7
    test2 = med_db.print_sum_date(20100101, 20120101)
    test2_len = len(test2)
    assert test2_len == 9
    test3 = med_db.print_sum_date(20100101, 20140101)
    test3_len = len(test3)
    assert test3_len == 14
    test4 = med_db.print_sum_date(20100101, 20120601)
    test4_len = len(test4)
    assert test4_len == 12


@pytest.mark.total
@pytest.mark.date
@pytest.mark.cal
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_date_total_small(small_db):
    ''' testing the date_total function with small_db'''
    test1 = small_db.date_total(20100101, 20110601)
    assert test1 == 110
    test2 = small_db.date_total(20100101, 20120101)
    assert test2 == 210
    test3 = small_db.date_total(20100101, 20120601)
    assert test3 == 280

@pytest.mark.total
@pytest.mark.date
@pytest.mark.cal
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_date_total_med(med_db):
    ''' testing the date_total function with med_db'''
    test1 = med_db.date_total(20100101, 20110601)
    assert test1 == 380
    test2 = med_db.date_total(20100101, 20120101)
    assert test2 == 480
    test3 = med_db.date_total(20100101, 20140101)
    assert test3 == 1050
    test4 = med_db.date_total(20100101, 20120601)
    assert test4 == 780
    

@pytest.mark.print
@pytest.mark.month
@pytest.mark.cal
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_month_small(small_db):
    ''' testing the print_sum_month function with small_db'''
    test1 = small_db.print_sum_month(6)
    test1_len = len(test1)
    assert test1_len == 3
    test2 = small_db.print_sum_month(1)
    test2_len = len(test2)
    assert test2_len == 4
    
@pytest.mark.print
@pytest.mark.month
@pytest.mark.cal
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_month_med(med_db):
    ''' testing the print_sum_month function with med_db'''
    test1 = med_db.print_sum_month(6)
    test1_len = len(test1)
    assert test1_len == 8
    test2 = med_db.print_sum_month(1)
    test2_len = len(test2)
    assert test2_len == 5
    test3 = med_db.print_sum_month(4)
    test3_len = len(test3)
    assert test3_len == 1

@pytest.mark.total
@pytest.mark.month
@pytest.mark.cal
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_month_total_small(small_db):
    ''' testing the month_total function with small_db'''
    test1 = small_db.month_total(6)
    assert test1 == 150
    test2 = small_db.month_total(1)
    assert test2 == 130
    
@pytest.mark.total
@pytest.mark.month
@pytest.mark.cal
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_month_total_med(med_db):
    ''' testing the month_total function with med_db'''
    test1 = med_db.month_total(6)
    assert test1 == 750
    test2 = med_db.month_total(1)
    assert test2 == 210
    test3 = med_db.month_total(4)
    assert test3 == 90


@pytest.mark.print
@pytest.mark.year
@pytest.mark.cal
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_year_small(small_db):
    ''' testing the print_sum_year function with small_db'''
    test1 = small_db.print_sum_year(2010)
    test1_len = len(test1)
    assert test1_len == 2
    test2 = small_db.print_sum_year(2011)
    test2_len = len(test2)
    assert test2_len == 2
    test3 = small_db.print_sum_year(2012)
    test3_len = len(test3)
    assert test3_len == 3

@pytest.mark.print
@pytest.mark.year
@pytest.mark.cal
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_year_med(med_db):
    ''' testing the print_sum_year function with med_db'''
    test1 = med_db.print_sum_year(2010)
    test1_len = len(test1)
    assert test1_len == 2
    test2 = med_db.print_sum_year(2011)
    test2_len = len(test2)
    assert test2_len == 5
    test3 = med_db.print_sum_year(2012)
    test3_len = len(test3)
    assert test3_len == 6
    test4 = med_db.print_sum_year(2013)
    test4_len = len(test4)
    assert test4_len == 1
    

@pytest.mark.total
@pytest.mark.year
@pytest.mark.cal
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_year_total_small(small_db):
    ''' testing the year_total function with small_db'''
    test1 = small_db.year_total(2010)
    assert test1 == 30
    test2 = small_db.year_total(2011)
    assert test2 == 80
    test3 = small_db.year_total(2012)
    assert test3 == 170

@pytest.mark.total
@pytest.mark.year
@pytest.mark.cal
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_year_total_med(med_db):
    ''' testing the year_total function with med_db'''
    test1 = med_db.year_total(2010)
    assert test1 == 30
    test2 = med_db.year_total(2011)
    assert test2 == 350
    test3 = med_db.year_total(2012)
    assert test3 == 530
    test4 = med_db.year_total(2013)
    assert test4 == 140


@pytest.mark.print
@pytest.mark.cat
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_cat_small(small_db):
    ''' testing the print_sum_cat function with small_db'''
    test1 = small_db.print_sum_cat('food')
    test1_len = len(test1)
    assert test1_len == 2
    test2 = small_db.print_sum_cat('ent')
    test2_len = len(test2)
    assert test2_len == 2
    test3 = small_db.print_sum_cat('travel')
    test3_len = len(test3)
    assert test3_len == 2
    test4 = small_db.print_sum_cat('bills')
    test4_len = len(test4)
    assert test4_len == 1

@pytest.mark.print
@pytest.mark.cat
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_print_sum_cat_med(med_db):
    ''' testing the print_sum_cat function with med_db'''
    test1 = med_db.print_sum_cat('food')
    test1_len = len(test1)
    assert test1_len == 3
    test2 = med_db.print_sum_cat('ent')
    test2_len = len(test2)
    assert test2_len == 3
    test3 = med_db.print_sum_cat('travel')
    test3_len = len(test3)
    assert test3_len == 4
    test4 = med_db.print_sum_cat('bills')
    test4_len = len(test4)
    assert test4_len == 4


@pytest.mark.total
@pytest.mark.cat
@pytest.mark.small
@pytest.mark.simple
@pytest.mark.transaction
def test_cat_total(small_db):
    ''' testing the cat_total function with small_db'''
    test1 = small_db.cat_total('food')
    assert test1 == 50
    test2 = small_db.cat_total('ent')
    assert test2 == 70
    test3 = small_db.cat_total('travel')
    assert test3 == 90
    test4 = small_db.cat_total('bills')
    assert test4 == 70

@pytest.mark.total
@pytest.mark.cat
@pytest.mark.med
@pytest.mark.simple
@pytest.mark.transaction
def test_cat_total_med(med_db):
    ''' testing the cat_total function with small_db'''
    test1 = med_db.cat_total('food')
    assert test1 == 180
    test2 = med_db.cat_total('ent')
    assert test2 == 160
    test3 = med_db.cat_total('travel')
    assert test3 == 270
    test4 = med_db.cat_total('bills')
    assert test4 == 440
