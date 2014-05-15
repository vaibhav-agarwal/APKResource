import MySQLdb as mdb
import MySQLdb.cursors
con=mdb.connect( host='localhost', user='loginname',
                 passwd='password', db='databasename',
                 cursorclass=MySQLdb.cursors.DictCursor)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS account1(id INT PRIMARY KEY AUTO_INCREMENT, account_name VARCHAR(200) , keystorefile VARCHAR(200))")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS apks1(id INT PRIMARY KEY AUTO_INCREMENT, apk_name VARCHAR(200) , account_name VARCHAR(150), sha1s text ,resource text, version VARCHAR(10) , time VARCHAR(30), loginid VARCHAR(30), package_name VARCHAR(100) )")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS coll1(id int(11) , resource_name VARCHAR(200), sha1s VARCHAR(200)) ")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS developer1(id INT PRIMARY KEY AUTO_INCREMENT, developer_name VARCHAR(200) , password VARCHAR(200), loginid VARCHAR(200) ,logintime VARCHAR(100))" )
con.commit();