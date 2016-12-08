#!/usr/bin/python
import pymysql.cursors
import cgi, cgitb
import loginAuthen as la
import re

def run(userID, password, password_confirm, phone, address):
	"""userID = 1231233;
	password = "wang1993";
	password_confirm = "wang1993";
	phone = "";
	address = """
	
	dbhost = "project498.cskimydhh1cu.us-west-2.rds.amazonaws.com"
	dbuser = "root";
	dbpassword = "wang1993"
	dbname = "retaildata";
        dbport = 3306
	connection = pymysql.connect(host=dbhost, user = dbuser, password=dbpassword, port=dbport, db = dbname);

	wrongNum = [];
	resultNum = checkNameRep(connection, userID);
	if resultNum!=0:
		wrongNum.append(resultNum);
	resultNum = checkPassword(password, password_confirm);
	if resultNum!=0:
		wrongNum.append(resultNum);
	if userID==None:
		wrongNum.append(4);
	if password==None or password_confirm==None:
		wrongNum.append(5);

	if wrongNum:
		generateWrongPage(wrongNum);
	else:
		sql = 'insert into customer values (%d, 0, "", "", "", "%s", "", "", "", "", "", "", "", 0, "%s", "", "2000-1-1", "", "", "", 0, 0, "", "2000-1-1", "", "", "", 0, "", "%s");' % (int(userID), str(address), str(phone), str(password));
		with connection.cursor() as cursor:
			cur = cursor.execute(sql);
		generateCorrectPage(userID);

def checkNameRep(conn, userID):
	sql = "select exists(select * from customer where customer_id=%d)" % int(userID);

	with conn.cursor() as cursor:
		cur = cursor.execute(sql);
		result = cursor.fetchone();
		if int(result[0])==1:
			return 1;
		else:
			return 0;

def checkPassword(password, password_confirm):
	if password!=password_confirm:
		return 2;
	elif not re.match("^[a-z].*", password):
		return 3;
	else:
		return 0;


def generateCorrectPage(userID):
	la.generateMain(userID);

def generateWrongPage(wrongNum):
	wrongInfoList = ['username has been registered', 'Two password not same', 'password format not correct', 'missing username', 'missing password']

	f = open("register.html", "r");
	print ("Content-type:text/html")
	print ("")
	
	while True:
		line = f.readline();
		if not line:
			break;

		if 1 in wrongNum and re.match(".*<input.*username.*", line):
			print ("%s" % line);
			print ('<font color="red">%s</font>' % wrongInfoList[0]);
		elif 2 in wrongNum and re.match('.*<input.*password.*', line):
			print ("%s" % line);
			print ('<font color="red">%s</font>' % wrongInfoList[1]);
		elif 3 in wrongNum and re.match('.*<input.*password.*', line):
			print ("%s" % line);
			print ('<font color="red">%s</font>' % wrongInfoList[2]);
		elif 4 in wrongNum and re.match(".*<input.*username.*", line):
			print ("%s" % line);
			print ('<font color="red">%s</font>' % wrongInfoList[3]);
		elif 5 in wrongNum and re.match('.*<input.*password.*', line):
			print ("%s" % line);
			print ('<font color="red">%s</font>' % wrongInfoList[1]);
		else:
			print ("%s" % line);

if __name__ == '__main__':
	form = cgi.FieldStorage() 
	userID = form.getvalue('username');
	password = form.getvalue('password');
	password_confirm = form.getvalue('password_confirm');
	phone = form.getvalue('phone');
	address = form.getvalue('address');

	if phone == None:
		phone = "";
	if address == None:
		address = "";

	run(userID, password, password_confirm, phone, address);



