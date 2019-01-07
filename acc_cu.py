#!/usr/bin/python
import MySQLdb, time, urllib, json
cautiousblocks = ["{{anonblock}}","{{schoolblock}}","vandalism", "school"]
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="dqscript",         # your username
                     passwd="BravoackenDelta",  # your password
                     db="production")        # name of the data base
cur = db.cursor()
cur.execute("SELECT id,status,forwardedip FROM production.request where status != 'Closed' and status != 'Hold' and status != 'CheckUser' and emailconfirm RLIKE 'confirmed';")
table = cur.fetchall()
db.close()
requestnumbers=list()
blocklist=list()
warnlist=list()
for row in table:
    #if search for comma
    requestnumbers.append(row[0])
    ip = row[2]
    try:
        ip = ip.split(", ")
    except:
        a=1 #just continue
    for item in ip:
        time.sleep(5)
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=&list=blocks&titles=&bkip="+item
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        try:blockdata=data["query"]["blocks"][0]
        except:continue
        reason = blockdata["reason"]
        ip = blockdata["user"]
        for blockreason in cautiousblocks:
            if blockreason in reason:
                warnlist.append(row[0])
            else:
                blocklist.append(row[0])
        try:cidr = ip.split("/")
        except:cidr = False
        print reason
        print "-------------"
