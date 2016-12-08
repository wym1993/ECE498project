#!/usr/bin/python
import cgi, cgitb
import pymysql
import re
def run():
    conn = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user="root", password="wang1993", db="retaildata", port=3306);
    with conn.cursor() as cursor:
        cur = cursor.execute("select * from loginInfo;");
        result = cursor.fetchone();
        result = [30,2]
        if result==None:
            generateWrongPage();
        else:
            generateTransHistory(int(result[0]))

def generateWrongPage():
    f = open("main.html", "r");
    print ("Content-type:text/html");
    print ("")
    while True:
        line = f.readline();
        if not line:
            break;
        if re.match('.*row content.*', line):
            print ('<h2><font colot="red"> You have no record, please register or login</font></h2>');
            print ('</div></body></html>')
            break;
        print ("%s" % line);

def generateTransHistory(userID):
    sql = 'select time_id, product_id, customer_id from agg_pl_01_sales_fact_1997 where customer_id=%d' % int(userID);
    conn = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user="root", password="wang1993", db="retaildata", port=3306);
    print ("Content-type:text/html");
    print ("")
    f = open("main.html", "r");
    while True:
        line = f.readline();
        if not line:
            break;
        if re.match('.*Login.*', line):
            line = '<li><p class="navbar-text">Welcome %s </p></li>'% (userID);
            print ("%s" % line);
            line = '<li><a href = "/main.html"><span class="glyphicon glyphicon-log-in">Logoff</span></a></li>'
        if re.match('.*Sign up.*', line):
            continue;
        if re.match('.*row content.*', line):
            print ("%s"% line);
            print ('<div class="col-sm-3"></div><div class="col-sm-6">');
            print ('<h2>Search History for %d</h2>'% userID);
            print ('<table class="table">');
            print ('<thread><th>Customer ID</th><th>Time ID</th><th>Product ID</th></thread><tbody>');
            break;
        print ("%s" % line);

    with conn.cursor() as cursor:
        cur = cursor.execute(sql);
        while True:
            result = cursor.fetchone();
            if not result:
                break;
            print ('<tr>');
            print ('<td>%s</td>' % result[2]);
            print ('<td>%s</td>' % result[0]);
            print ('<td>%s</td>' % result[1]);
            print ('</tr>')         
        
        print ('</tbody></table></div><div class="col-sm-3"></div></div></body></html>')


if __name__=='__main__':
    #generateWrongPage(); 
    run();
