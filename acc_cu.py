#!/usr/bin/python
import MySQLdb, time, json
from urllib2 import Request, urlopen, URLError, HTTPError

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="dqscript",         # your username
                     passwd="BravoackenDelta",  # your password
                     db="production")        # name of the data base
cur = db.cursor()
cur.execute("SELECT id,status,forwardedip FROM production.request where status != 'Closed' and status != 'Hold' and status != 'CheckUser' and emailconfirm RLIKE 'confirmed';")
table = cur.fetchall()
db.close()
for row in table:
    #if search for comma
    ip = row[2]
    try:
        ip = ip.split(", ")
    except:
        a=1 #just continue
    for item in ip:
        time.sleep(5)
        req = Request("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=&list=blocks&titles=&bkip="+item)
        try:
            response = json.loads(urlopen(req).decode())
        except HTTPError as e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError as e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
            print response
            break
        break
    break
