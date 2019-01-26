#!/usr/bin/python
import MySQLdb, time, urllib, json, datetime
cautiousblocks = ["{{anonblock}}","{{schoolblock}}","vandalism", "school"]
proxyblocks = ["{{blockedproxy}}","{{webhostblock}}","{{colocationwebhost}}"]
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="dqscript",         # your username
                     passwd="BravoackenDelta",  # your password
                     db="production")        # name of the data base
cur = db.cursor()
cur.execute("CREATE SCHEMA IF NOT EXISTS dqscript;")
cur.execute("CREATE TABLE IF NOT EXISTS dqscript.blockcheck (id INT(11)) ENGINE=InnoDB;")
cur.execute("SELECT r.id,r.status,r.forwardedip FROM production.request r where r.status != 'Closed' and r.status != 'Hold' and r.status != 'Checkuser' and r.emailconfirm RLIKE 'confirmed' and not exists (SELECT 1 FROM dqscript.blockcheck bc WHERE bc.id = r.id);")
table = cur.fetchall()
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
        except:
            cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
            db.commit()
            continue
        reason = blockdata["reason"]
        try:acc = blockdata["nocreate"]
        except:
            cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
            db.commit()
            continue
        if "ACC ignore" in reason:
            cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
            db.commit()
            continue
        ip = blockdata["user"]
        first = True
        warn=False
        for blockreason in cautiousblocks:
            if blockreason.lower() in reason.lower():
                warn = True
                cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
                db.commit()
                continue
        for blockreason in proxyblocks:
            if blockreason.lower() in reason.lower():
                warn = True
                cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
                db.commit()
                cur.execute("UPDATE production.request SET status='Proxy' WHERE id="+str(row[0])+";")
                db.commit()
                cur.execute("INSERT INTO production.comment (time, user, comment, visibility, request) VALUES (\""+time.strftime('%Y-%m-%d %H:%M:%S')+"\", '1733', \"Block detected requiring proxy check\", \"user\", "+str(row[0])+");")
                db.commit()
                cur.execute("INSERT INTO production.log (objectid, objecttype, user, action, timestamp) VALUES ("+str(row[0])+", \"Request\", 1733, \"Deferred to proxy check\", \""+time.strftime('%Y-%m-%d %H:%M:%S')+"\");")
                db.commit()
                continue
        if warn:continue
        blocklist.append(row[0])
        try:cidr = ip.split("/")
        except:cidr = False
        cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
        db.commit()
        cur.execute("UPDATE production.request SET status='Checkuser' WHERE id="+str(row[0])+";")
        db.commit()
        cur.execute("INSERT INTO production.comment (time, user, comment, visibility, request) VALUES (\""+time.strftime('%Y-%m-%d %H:%M:%S')+"\", '1733', \"Block detected requiring CU check\", \"user\", "+str(row[0])+");")
        db.commit()
        time.sleep(1)
        cur.execute("INSERT INTO production.log (objectid, objecttype, user, action, timestamp) VALUES ("+str(row[0])+", \"Request\", 1733, \"Deferred to checkusers\", \""+time.strftime('%Y-%m-%d %H:%M:%S')+"\");")
        db.commit()
        cur.execute("INSERT INTO dqscript.blockcheck SELECT "+str(row[0])+" FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM dqscript.blockcheck WHERE id = "+str(row[0])+");")
        db.commit()
db.close()
