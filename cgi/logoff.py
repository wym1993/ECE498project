#!/usr/bin/python
import cgi, cgitb
import loginAuthen as la
import re
import os
import pymysql

if __name__=='__main__':
    conn = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user="root", password="wang1993", db="retaildata", port=3306);
    with conn.cursor() as cursor:
        cur = cursor.execute("delete from loginInfo");
    print ("Content-type:text/html");
    print ("")
    f = open("main.html", 'r');
    while True:
        line = f.readline();
        if not line:
            break;
        print ("%s" % line);

