#!/usr/bin/python
# coding:utf-8
__author__ = 'kerwinaj'

import sys
import MySQLdb

'''
TransferMoney.py zhangsan lisi 100
'''

class MoneyTransfer(object):
    def __init__(self, conn):
        self.conn = conn

    def transfer(self, source_account_id, target_account_id, money):
        try:
            self.check_account_available(source_account_id)
            self.check_account_available(target_account_id)
            self.has_enough_money(source_account_id, money)
            self.reduce_money(source_account_id, money)
            self.add_money(target_account_id, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print "raise from transfer"
            raise e

    def check_account_available(self, account_id):
        cursor = self.conn.cursor()

        try:
            sql = "select * from account where account_id='%s'" % account_id
            print "check_account_available:" + sql
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("帐号%s不存在" % account_id)
        except Exception as e:
            # 会自动 raise exception 到调用的地方, 所以不加这段except也可以的
            print "raise from check_account_available"
            raise e
        finally:
            cursor.close()

    def has_enough_money(self, account_id, money):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where account_id='%s' and money > %s" % (account_id, money)
            print "has_enough_money:" + sql
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("帐号%s没有足够的钱" % account_id)
        finally:
            cursor.close()

    def reduce_money(self, account_id, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money-%s where account_id = '%s'" % (money, account_id)
            print "reduce_money:" + sql
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception("帐号%s扣款失败" % account_id)
        finally:
            cursor.close()

    def add_money(self, account_id, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money+%s where account_id = '%s'" % (money, account_id)
            print "add_money:" + sql
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception("帐号%s加款失败" % account_id)
        finally:
            cursor.close()


if __name__ == "__main__":
    source_account_id = sys.argv[1]
    target_account_id = sys.argv[2]
    money = sys.argv[3]

    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user="uzone", passwd="uzone", db="test")
    money_transfer_obj = MoneyTransfer(conn)

    try:
        money_transfer_obj.transfer(source_account_id, target_account_id, money)
    except Exception as e:
        print "__main__ error:" + str(e)
    finally:
        conn.close()