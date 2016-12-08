#!/usr/bin/python
import pymysql
import re

def run():
    print ("Content-type:text/html")
    print ("")
    conn = pymysql.connect(host="project498.cskimydhh1cu.us-west-2.rds.amazonaws.com", user="root", password="wang1993", db="retaildata", port=3306);
    f = open("main.html", "r");
    while True:
        line = f.readline();
        if not line:
            break;
        if re.match('.*row content.*', line):
            print ("%s" % line);
            print ('<div class="col-sm-3"></div><div class="col-sm-6">');
            print ('<h2>Item List</h2>');
            print ('<table class="table">');
            print ('<thread><tr><th>product ID</th><th>Product Name</th><th>Cost</th></tr></thread><tbody>');
            break;
        print ("%s" % line);
    product_id = [];
    store_cost_sum = [];
    fact_count = [];
    with conn.cursor() as cursor:
        sql = 'select distinct product_id, store_cost_sum, fact_count from agg_pl_01_sales_fact_1997 group by product_id;';
        cur = cursor.execute(sql);
        while True:
            result = cursor.fetchone();
            if not result:
                break;
            product_id.append(int(result[0]));
            store_cost_sum.append(float(result[1]));
            fact_count.append(float(result[2]));

        for i in range(len(product_id)):
            sql = 'select product_name from product where product_id=%d' % product_id[i];
            cur = cursor.execute(sql);
            result = cursor.fetchone();
            price = store_cost_sum[i]/fact_count[i];
            print("<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (product_id[i], result[0], price));
            #if product_id[i]==50:
            #   break;

    print('</tbody></table></div><div class="col-sm-3"></div></div></body></html>')

if __name__ == '__main__':
    run();
