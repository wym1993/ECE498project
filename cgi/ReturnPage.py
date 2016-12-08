#!/usr/bin/python
import cgi, cgitb
import random
import re

def run(userID, N, recommendList, itemDic):
	#X=[125,145,202,222,279,299,356,376,433,452]
	X=[280, 318, 386, 424, 492, 530, 598, 636, 704, 742]
        Y=[]
	Y.append(670)
	for i in range(1,19):
		Y.append(670-i*33)

	I=[]
	J=[]
	#N=[0, 1, 2, 3, 4, 23, 22, 21, 20, 19, 38, 57, 76, 77, 78, 79, 80, 81, 82, 83, 84, 103, 104, 105, 106, 107, 108, 109, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 99, 98, 97, 96, 95, 114, 133, 152, 153, 154, 153, 152, 133, 114, 115, 116, 115, 114, 95, 76, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 94, 113, 132, 151, 170, 189]
	for a in range(0,len(N)):
		x = int(N[a]/19)
		y = int(N[a]%19)

		i = X[x]
		j = Y[y]


		I.append(i)
		J.append(j)

	print ("Content-type:text/html")
	print ("")
	f = open("main.html", "r");
	while True:
		line = f.readline();
		if not line:
			break;
		if int(userID)!=0:
			if re.match('.*name="userID".*', line):
				line = '<input type="hidden", name="userID", value="%d">' % int(userID);
			elif re.match('.*Login.*', line):
				line = '<li><p class="navbar-text"> Welcome %s</p> </li>' % userID;
                                print ("%s" % line);
                                line = '<li><a href="/main.html"><span class="glyphicon glyphicon-log-in">Logoff</span></a></li>'
			elif re.match(".*Sign up.*", line):
				continue;

		if re.match('.*b.jpg.*', line):
			print ('<svg height="100%" width="100%">')
			print ('<image xlink:href="/b.jpg" src = "/b.jpg" x="0" y="0" height="700" width="700"/>')
			#print ('<image xlink:href="/b.jpg" src="/b.jpg" class="rounded">')
                        for c in range(0,len(I)-1):
                                print ('<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:rgb(255,0,0);stroke-width:2" />' % (I[c]-175,J[c]-25,I[c+1]-175,J[c+1]-25))
				
			for key in itemDic.keys():
				x = int(itemDic[key]/19);
				y = int(itemDic[key]%19);
				i = X[x];
				j = Y[y];
				sp = key.split(" ");
				print ('<circle cx="%d" cy="%d" r="2" stroke="black" stroke-width="3" fill="red" />' % (i-175,j-25))
				ran = random.randint(0,1);
				if ran == 0:
					ran = -2;
				elif ran==1:
					ran = 2;
				print ('<text x="%d" y="%d" fill="black">%s</text>' % (i-175+ran, j-25, sp[-1]))

			print ('</svg>')
		else:
			print ("%s" % line);

		if re.match('.*</form>.*', line):
			print ('<h4> We highly recommend you to buy: </h4>');
			print ('<ul>');
			num = 0;
			for recom in recommendList:
				num+=1;
				print ('<li>%s</li>' % recom);
				if num==3:
    					break;
                        print ('</ul>')
	#itemList = [123, "CDR Grape Jelly"];
	#routePos = run(itemList)2
