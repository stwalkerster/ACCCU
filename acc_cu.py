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
        if "ACC ignore" in reason:continue
        ip = blockdata["user"]
        first = True
        warn=False
        for blockreason in cautiousblocks:
            if blockreason in reason:
                warn=True
        if warn:
            warnlist.append(row[0])
            print "WARN: " + reason
        else:
            blocklist.append(row[0])
            print "NONE: " + reason
        try:cidr = ip.split("/")
        except:cidr = False
        print "-------------"
