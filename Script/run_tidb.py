#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# System modules
from threading import Thread
import time
import mysql.connector
import argparse
## If Python is version 2.7, encoding problems can reload sys configuration
try:
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

def mysql_exe():
    args = parser_args()
    try:
        connection = mysql.connector.connect(host=args.host,
                                 user=args.user,
                                 password=args.password,
                                 port=args.port,
                                 charset='utf8mb4',
                                 database=args.database)
    except all as error:
        print("error is ", error)
    finally:
        pass

    try:
        # i_sql = open("insert.sql","r+").read()
        # d_sql = open("delete.sql","r+").read()
 
        d_sql = "DELETE from t3 limit {}"
        cursor = connection.cursor()
        cursor.execute("SET NAMES utf8mb4")
        for i in range(args.limit):
            cursor.execute("INSERT INTO t3 (cname,start_time,cid) values (RAND() * 10000,now(3), RAND() * 10000)")
        print("insert into {} lines sucessfull~".format(args.limit))
        if args.mode == 'id':
            cursor.execute("DELETE from t3 limit {}".format(args.limit))
            print("delete {} lines sucessfull~".format(args.limit))
        cursor.close()
        connection.commit()
    except all as error:
        print("error is ", error)
    finally:
        connection.close()
    a = 'mysql'
    return a

def main():
    args = parser_args()
    threads = []
    for i in range(int(args.thread_num)):
        threads.append(Thread(target=mysql_exe,))
        print("execute thread: {}".format(i))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def parser_args():
    parser = argparse.ArgumentParser(description="Test case for cq")
    parser.add_argument("--host", dest="host", help="TiDB's host",default='127.0.0.1')
    parser.add_argument("-P", dest="port", help="TiDB's port",default=4000)
    parser.add_argument("-u", dest="user", help="TiDB's user",default="root")
    parser.add_argument("-p",dest="password", help="TiDB's passwd",default='')
    parser.add_argument("-b",dest="database",help="TiDB's database", default="test")
    parser.add_argument("--thread",dest="thread_num",help="execute thread",default=5)
    parser.add_argument("--exe",dest="range_num",help="Execution times",default=10)
    parser.add_argument("--mode",dest="mode",help="Test Case: id is insert and delete,Only test insert by default",default="insert")
    parser.add_argument("--limit",dest="limit",help="How many rows to delete or insert", default=1000)
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parser_args()
    range_num, thread_num = args.range_num, args.thread_num
    st = time.time()
    for i in range(int(range_num)/int(thread_num)):
        main()
    print('execute number: {}'.format(range_num))
    ct = time.time() - st
    print("total cost time: {}s").format(ct)
    print("avg is: {}s").format(ct/int(range_num))
