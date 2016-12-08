#!/usr/bin/python
import cgi, cgitb
import RouteMain as rm
import recommend as rd
import ReturnPage as rp

if __name__ == '__main__':
	itemList = [];
	form = cgi.FieldStorage() 
	userID = form.getvalue('userID')
	#print ("User id is ", userID)
	for i in range(10):
		string = "textbox" + "%d" % (i+1);
		oneItem = str(form.getvalue(string));
		if oneItem!="None":
			itemList.append(oneItem);
        itemDic, newRou = rm.run(userID, itemList);
        itemDicList = [];
        for it in itemDic.keys():
            itemDicList.append(itemDic[it]);
        final_result=rd.run(itemDicList);
	"""print "Content-type:text/html"
        print ""
        print "<html><body>";
        print "%s" % itemDic;
        print "</body></html>"""
        rp.run(userID, newRou, final_result, itemDic);
	#rp.run(newRou)
