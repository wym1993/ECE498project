#!/usr/bin/python
import pymysql.cursors
import random
import sys

def readTrans(itemList):
    trans = list();
    tcPair = []
    connection = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user = "root", password="wang1993",port=3306, db = "retaildata");
    # Get subclass product pair:
    pair = dict();
    sql = "select product_class_id, product_id from product;";
    with connection.cursor() as cursor:
        cur = cursor.execute(sql);
        while True:
            result = cursor.fetchone();
            if result:
                pair[int(result[1])]=int(result[0]);
            else:
                break;
    
    for item in itemList:
        sql = "select time_id, customer_id from agg_pl_01_sales_fact_1997 where product_id=%d;" % (item);  # need to change the RouteMain.py to get the product_id for items
        with connection.cursor() as cursor:
            cur = cursor.execute(sql);
            while True:
                result = cursor.fetchone()
                if result:
                    tcPair.append((int(result[0]), int(result[1])))
                else:
                    break;

    for time, cid in tcPair:
        trans.append(list())
        sql = "select product_id from agg_pl_01_sales_fact_1997 where time_id=%d and customer_id=%d;" % (time, cid);
        with connection.cursor() as cursor:
            cur = cursor.execute(sql);
            while True:
                result = cursor.fetchone()
                if result:
                    trans[-1].append(pair[int(result[0])]);
                else:
                    break;
    transSet = []
    for tr in trans:
        transSet.append(set(tr));
    itemListCopy = [];
    for item in itemList:
        itemListCopy.append(pair[item]);
    return transSet, itemListCopy;


def support_count(orders, item_set):
    """Calculate support count of item set from orders 2D list"""
    count = 0

    for order in orders:
        if item_set.issubset(order):
            # print("Found {} in {}".format(item_set, order))
            count += 1
        else:
            # print("Didn't find {} in {}".format(item_set, order))
            pass
    return count


def support_frequency(orders, item_set):
    """Calculate support frequency of item set from orders 2D list"""
    N = len(orders)
    return support_count(orders, item_set)/float(N)


def confidence(orders, left, right):
    """Calculate confidence of item set from orders 2D list"""
    right_count = support_count(orders, right)
    left = right.union({left})
    left_count = support_count(orders, left)
    result = left_count*1.0/right_count
    return result


def apriori(orders, product_ids):
    candidate_items = set()
    for items in orders:
        candidate_items = candidate_items.union(items)
    
    result= []

    for product_id in product_ids:
        
        maxConf = [0.0, 0.0];
        maxConfItem = [-1, -1];
        maxSup = [0.0, 0.0];
        maxSupItem = [-1, -1];
        for item in candidate_items.difference(product_ids):
            conf = confidence(orders, item, {product_id});
            if conf>maxConf[0]:
                maxConf[1] = maxConf[0];
                maxConf[0] = conf;
                maxConfItem[1] = maxConfItem[0];
                maxConfItem[0] = item;
            elif conf>maxConf[1] and conf<maxConf[0]:
                maxConf[1] = conf;
                maxConfItem[1] = item;
            sup = support_frequency(orders, {item}.union({product_id}));
            if sup>maxSup[0]:
                maxSup[1] = maxSup[0];
                maxSup[0] = sup;
                maxSupItem[1] = maxSupItem[0];
                maxSupItem[0] = item;
            elif sup>maxSup[1] and sup<maxSup[0]:
                maxSup[1] = sup;
                maxSupItem[1] = item;
        for it in maxConfItem:
            if not it in result:
                result.append(it);
        for it in maxSupItem:
            if not it in result:
                result.append(it);
    resultPro = []
    connection = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user = "root", password="wang1993", port=3306, db = "retaildata");
    for re in result:
        sql = "select product_name from product where product_class_id=%d;" % re;
        temp = [];
        with connection.cursor() as cursor:
            cursor.execute(sql);
            while True:
                result = cursor.fetchone();
                if result:
                    temp.append(result[0]);
                else:
                    break;
        rand = random.randint(0,len(temp)-1);
        resultPro.append(temp[rand]);

    return resultPro;

def run(itemList):
    data, itemList = readTrans(itemList);
    final_results =apriori(data, itemList);
    return final_results;
