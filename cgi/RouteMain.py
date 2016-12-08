#!/usr/bin/python
import Genetic_new_new as gen
import networkx as nx
import pymysql.cursors
import cgi, cgitb
import datetime
import re

def run(userID, itemList):
	itemDic = findLoc(userID, itemList);
	#itemDic = list(set(itemDic));
	#itemDic  = dict(a=21, b=89)
	g = nx.Graph();
	g.add_nodes_from(range(190));
	g = nx.read_edgelist('edgelist', nodetype=int);

	sg = nx.Graph();
	sg.add_node(0);
	sg.add_node(189);
	
	for key in itemDic:
		sg.add_node(itemDic[key]);

	for node1 in sg.nodes():
		for node2 in sg.nodes():
			path = nx.shortest_path(g, source=node1,  target=node2);
			#print ("node1 %d node2 %d path %s and length %d" % (node1, node2, path, len(path)));
			dis = len(path);
			sg.add_edge(node1, node2, distance=dis, path=path);

	route = gen.run(sg);
	routePos = []
	for i in range(0,len(route)-1):
		routePos.append(sg[route[i+1]][route[i]]['path']);
		
	newRou = formRoute(0,189, routePos)
	return itemDic, newRou

def findLoc(userID, itemList):
	dbhost = "project498.cskimydhh1cu.us-west-2.rds.amazonaws.com"
	dbuser = "root";
	dbpassword = "wang1993"
	dbname = "retaildata";
        dbport = 3306
	connection = pymysql.connect(host=dbhost, user = dbuser, password=dbpassword, port=dbport, db = dbname);
	itemDic = dict();

	for itemInd in range(len(itemList)):
		sql = 'select product_class_id from product where product_name = "%s";' % itemList[itemInd];
		with connection.cursor() as cursor:
			cur = cursor.execute(sql);
			result = cursor.fetchone();
			if result==None:
                                ambTest = ambiguousMatch(itemList[itemInd], connection);
                                if ambTest[0]==0:
                                    generateWrongMain(userID, itemList[itemInd]);
				else:
                                    itemDic[itemList[itemInd]] = ambTest[1];
			else:
				sql2 = 'select product_location from product_class where product_class_id=%d;' % result[0];
				cur = cursor.execute(sql2);
				loc = cursor.fetchone();
				itemDic[itemList[itemInd]] = loc[0];
	updateTrans(userID, itemList, itemDic, connection)
	return itemDic

def updateTrans(userID, itemList, itemDic, connection):
        t = datetime.datetime.now();
	with connection.cursor() as cursor:
                #for it in range(len(itemList)):
                #        sql2 = 'insert into search_history values(%d, "%d-%d-%d", %d);' % (int(userID), t.year, t.month, t.day, int(itemDic[itemList[it]]));
                #        cur = cursor.execute(sql2)
		for it in range(len(itemList)):
		        sql2 = 'insert into agg_pl_01_sales_fact_1997 values(%d, 0, %d, 0.0000, 0.0000, 0.0000, 0)' % (int(itemDic[itemList[it]]), int(userID));
		        cur = cursor.execute(sql2);

def formRoute(start, end, routePos):
	newRou = [];
	newRou.append(start);
	for route in routePos:
		if route[0]==newRou[-1]:
			newRou = appNormal(newRou, route);
		elif route[-1] == newRou[-1]:
			newRou = appReverse(newRou, route);

	if end == newRou[-1]:
		return newRou;
	else:
		return routePos;

def appNormal(newRou, route):
	for it in range(1,len(route)):
		newRou.append(route[it]);

	return newRou;

def appReverse(newRou, route):
	route.reverse();
	for it in range(1,len(route)):
		newRou.append(route[it]);

	return newRou;

def ambiguousMatch(item, conn):
    sql = 'select product_id, product_name from product;';
    with conn.cursor() as cursor:
        cur = cursor.execute(sql)
        while True:
            result = cursor.fetchone();
            if not result:
                break;
            pattern = ".*"+item+".*";
            if re.match(pattern, str(result[1])) or re.match(pattern, str(result[1]).lower()):
                return [1,int(result[0])];
    return [0, 0];
            

def generateWrongMain(userID, item):
    f = open("main.html", "r");
    print ("Content-type:text/html");
    print ("")
    while True:
        line = f.readline();
        if not line:
            break;

        if int(userID) !=0:
            if re.match(".*Login.*", line):
                print ( '<li><p class="navbar-text">Welcome %s</p></li>'% int(userID));
                line = '<li><a href="/main.html"><span class="glyphicon glyphicon-log-in">Logoff</span></a></li>';
            if re.match('.*Sign up.*', line):
                continue;
        if re.match('.*type="hidden".*name="userID".*', line):
            line = '<input type="hidden", name="userID", value="%d">' % (int(userID));
        elif re.match(".*value='Add Button'.*", line):
            print ('<font color="red">**%s cannot be found**</font></br>' % str(item))

        print ("%s" % line);

