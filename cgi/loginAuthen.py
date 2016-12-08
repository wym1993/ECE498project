#!/usr/bin/python
import pymysql.cursors
import cgi, cgitb
import re

def checkUser(userID, password):
	dbhost = "project498.cskimydhh1cu.us-west-2.rds.amazonaws.com"
	dbuser = "root";
	dbpassword = "wang1993"
	dbname = "retaildata";
        dbport = 3306
	connection = pymysql.connect(host=dbhost, user = dbuser, password=dbpassword,port=dbport, db = dbname);
	sql = 'select password from customer where customer_id = %d;' % int(userID);
	with connection.cursor() as cursor:
		cur = cursor.execute(sql);
		result = cursor.fetchone();
		if result==None:
			return 0;
		elif result[0]!=password:
			return 0;
		else:
			return 1;

def callReturn(userID, password):
	print ("Content-type:text/html")
	print ("")
	print ("user id is %d" % int(userID));
	print ("password is %s" % password);
	print ("</body></html>")

def generateMain(userID):
        conn = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user="root", password="wang1993", db="retaildata", port=3306);
        with conn.cursor() as cursor:
            sql = 'insert into loginInfo values(%d)' % int(userID);
            cur = cursor.execute(sql);
	print ("Content-type:text/html")
	print ("")
	f = open("main.html", "r");
	while True:
		line = f.readline();
		if not line:
			break;
		if re.match('.*type="hidden".*name="userID".*', line):
			print ('<input type="hidden", name="userID", value="%d">' % int(userID));
		elif re.match('.*Login.*', line):
			#line = '<li><font color="white"> Welcome %s</font> </li>' % userID;
                        line = '<li><p class="navbar-text">Welcome %s</p></li>' % userID
			print ("%s" % line);
                        line = '<li><a href="/main.html"><span class="glyphicon glyphicon-log-in">Logoff</span></a></li>'
                        print ("%s" % line)
		elif re.match(".*Sign up.*", line):
				continue;
		else:
			print ("%s" % line);


def generateLogin():
	print ("Content-type:text/html")
	print ("")
	
	f = open("login.html", "r");
	while True:
		line = f.readline();
		if not line:
			break;
		if re.match('.*<button.*', line):
			print ('<br><font color="red">You have the wrong username or password</font>')
			print ("<br>%s" % line);
		else:
			print ("%s" % line);


if __name__ == '__main__':
	form = cgi.FieldStorage() 
	userID = form.getvalue('userID')
	password = str(form.getvalue('password'));
        #userID = 1;
	#password = "1111";
	#callReturn(userID, password);
	deter = checkUser(userID, password);
        #callReturn(userID,deter)
	if deter==1:
		generateMain(userID);
	else:
		generateLogin();
