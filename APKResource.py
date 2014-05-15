import MySQLdb as mdb                                          #For MySQL in Python
import MySQLdb.cursors
import zipfile                                                 #To extract MANIFEST.MF from apk  
import datetime
import md5                                                     #For security
import subprocess                                              #For executing shell commands through python
import boto                                                    #For using services of Amazon SES 
import json

from email.mime.text import MIMEText                           #For attachments in email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

#import resourcedatabase1                                       #To create database tables
con=""
cur=""

con=mdb.connect( host='localhost', user='loginname',                 # MySQL Database connection 
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)                     

cur = con.cursor()


from flask import Flask, render_template ,request,url_for,redirect,session
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'               # For Session 

#################################################################################
 
developername=""                                                # List of Global Variables
coll={}
collflag=0
names=""
times=""
cc=""
aa=""
aaa=""
sha=""
resource=""
fail=0
incorrectfile=0
uploadsuccess=0
testsuccess=0
passchange=0
accountexist=0
accountnotexist=0
developerexist=0
developernotexist=0
saveadmin=0
devapk=0
invalidinput=0
accountcreate=0
accountdelete=0
developeradd=0
developerdelete=0
adminapkupload=0
canupdatecollisions=0
apktoupdate=0
apktoupdateversion=0
version=""
xxx=""
changelogempty=0
emailfrom=0
connection=""
askemail=""
emaildomain1=""
msg=""

#################################################################################

@app.route('/')                                                 #Endpoint for mainpage    
def mainpage ():

    global fail
    global con
    global cur
                                                #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()


        

    try:
        print session['username']
        session.pop('username', None)
        print 'yes'
        print session['username']
    except:
        print 'ko'


    if fail==1:                                                #Print Your login failed !                                              
        fail=0                                                 #Please Retry !! 
        return render_template('main.html',fails=1)
    else:
        fail=0
        return render_template('main.html')

#################################################################################

@app.route('/admin',methods=['POST','GET'])                      #Endpoint for Admin     
def admin():
    global coll
    global times
    global names
    global collflag
    global accountexist
    global accountnotexist
    global developerexist
    global developernotexist
    global saveadmin
    global devapk
    global invalidinput
    global accountcreate
    global accountdelete
    global developeradd
    global developerdelete
    global adminapkupload
    global incorrectfile
    global canupdatecollisions
    global apktoupdate
    global apktoupdateversion
    global xxx
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()



    if request.method=='POST':

        if 'username' in session:

            if session['username']=='admin':

                flag=0

                coll={}
                times=""
                names=""
                collflag=0					

                cur.execute("SELECT id,account_name FROM account1")                #To get all accounts 
                con.commit()
                a=cur.fetchall()
                al=len(a)

                cur.execute("SELECT id,developer_name,loginid FROM developer1 ")   #To get all developers
                con.commit()
                b=cur.fetchall()
                dl=len(b)

                cur.execute("SELECT package_name,account_name,apk_name,version,time,developer_name FROM apks1,developer1 WHERE apks1.loginid=developer1.loginid ")                                                
                con.commit()
                apk=cur.fetchall()                                                #To get all uploaded packages
                apkl=len(apk)

                params={}
                params['accountnames']=a
                params['developernames']=b
                params['apks']=apk
                params['alength']=al
                params['dlength']=dl
                params['apklength']=apkl

                if accountexist==1:                                              #Print "Account Already Exists ! "
                    accountexist=0
                    params['accountexist']=1

                if accountnotexist==1:                                           #Print "Account Does Not Exist"
                    accountnotexist=0
                    params['accountnotexist']=1

                if developerexist==1:                                            #Print "Developer Already Exists! "
                    developerexist=0
                    params['developerexist']=1

                if developernotexist==1:                                         #Print "Developer Does Not Exist" 
                    developernotexist=0
                    params['developernotexist']=1

                if saveadmin==1:                                                 #Print "Cannot Delete Admin"
                    saveadmin=0
                    params['saveadmin']=1
                                                                                 #Print "No Uploaded Apks"   
                if devapk==1:                                                                                                         
                    devapk=0
                    params['devapk']=1

                if invalidinput==1:                                              #Print "Invalid Input , Please Try Again!"  
                    invalidinput=0
                    params['invalidinput']=1

                if accountcreate==1:                                             #Print "Account Created Successfully"
                    accountcreate=0 
                    params['accountcreate']=1


                if accountdelete==1:                                             #Print "Account Deleted Successfully"
                    accountdelete=0
                    params['accountdelete']=1
 
                if developeradd==1:                                              #Print "Developer Added Successfully"
                    developeradd=0
                    params['developeradd']=1

                if developerdelete==1:                                           #Print "Developer Deleted Succesfully"
                    developerdelete=0
                    params['developerdelete']=1

                if adminapkupload==1:                                            #Print "Package Successfully Uploaded"
                    adminapkupload=0
                    params['adminapkupload']=1

                if incorrectfile==1:                                             #Print "Incorrect file type ! Please try again!" 
                    incorrectfile=0
                    params['incorrect']=1

                if canupdatecollisions==1:                                       #Print "Cannot Update Collisions"
                    canupdatecollisions=0
                    params['canupdate']=1

                if canupdatecollisions==3:                                       #Print "Collisions Updated"
                    canupdatecollisions=0
                    params['canupdate1']=1

                if canupdatecollisions==2:                                       

                    canupdatecollisions=0
                    cur.execute("SELECT resource from apks1 WHERE package_name='"+apktoupdate+"' AND version='"+apktoupdateversion+"'")
                    con.commit()
                    z=cur.fetchall();

                    x=z[0]['resource'].split(',')
                    print "resources are",x
                    xx=[]
                    cur.execute("SELECT resource_name from coll1 ")
                    con.commit()
                    r=cur.fetchall();

                    for i in range(len(x)):
                        for j in range(len(r)):
                            if x[i]==r[j]['resource_name']:
                                xx.append(x[i])

                    xxx=list(set(x) - set(xx))

                    params['updateresource']=xxx                               #Print those resources which are not present in the      
                                                                               # collision table 


                try:
                    a=request.form['developername']                            #To add a new developer
                    flag=1
                except:
                    try:
                        a=request.form['accountname']                          #To add a new account
                        flag=2
                    except:
                        flag=0

                logintime=session['logintime']

                if flag==1:
                    cur.execute("SELECT package_name,account_name,apk_name,version,time,developer_name FROM apks1,developer1 WHERE apks1.loginid=developer1.loginid AND developer1.developer_name='"+a+"'")
                    con.commit()
                    s=cur.fetchall()
                    sl=len(s)
                    print s,sl

                    if len(s)<1:
                        devapk=1
                        return redirect(url_for('admin'))

                    else:
                        params['searchdev']=s
                        params['searchdevlength']=str(sl)
                        return render_template('admin.html',param=params,log=logintime)

                if flag==2:
                    cur.execute("SELECT package_name,account_name,apk_name,version,time,developer_name FROM apks1,developer1 WHERE apks1.loginid=developer1.loginid AND apks1.account_name='"+a+"'")
                    con.commit()
                    sa=cur.fetchall()
                    sla=len(sa)
                    print sa,sla

                    if len(sa)<1:
                        devapk=1
                        return redirect(url_for('admin'))
                    else:
                        params['searchaccount']=sa
                        params['searchaccountlength']=str(sla)
                        return render_template('admin.html',param=params,log=logintime)

            return redirect(url_for('mainpage'))

        else:
            return redirect(url_for('mainpage'))


    if request.method=='GET':    

        if 'username' in session:

            if session['username']=='admin':

                coll={}
                times=""
                names=""
                collflag=0

                cur.execute("SELECT id,account_name FROM account1")
                con.commit()
                a=cur.fetchall()
                al=len(a)

                cur.execute("SELECT id,developer_name,loginid FROM developer1 ")
                con.commit()
                b=cur.fetchall()
                dl=len(b)

                cur.execute("SELECT package_name,account_name,apk_name,version,time,developer_name FROM apks1,developer1 WHERE apks1.loginid=developer1.loginid ")
                con.commit()
                apk=cur.fetchall()
                apkl=len(apk)

                params={}
                params['accountnames']=a
                params['developernames']=b
                params['apks']=apk
                params['alength']=al
                params['dlength']=dl
                params['apklength']=apkl

                if accountexist==1:
                    accountexist=0
                    params['accountexist']=1

                if accountnotexist==1:
                    accountnotexist=0
                    params['accountnotexist']=1

                if developerexist==1:
                    developerexist=0
                    params['developerexist']=1

                if developernotexist==1:
                    developernotexist=0
                    params['developernotexist']=1

                if saveadmin==1:
                    saveadmin=0
                    params['saveadmin']=1

                if devapk==1:
                    devapk=0
                    params['devapk']=1

                if invalidinput==1:
                    invalidinput=0
                    params['invalidinput']=1
                    print 'yes'

                if accountcreate==1:
                    accountcreate=0
                    params['accountcreate']=1
                    print "param is" ,params['accountcreate']

                if accountdelete==1:
                    accountdelete=0
                    params['accountdelete']=1

                if developeradd==1:
                    developeradd=0
                    params['developeradd']=1

                if developerdelete==1:
                    developerdelete=0
                    params['developerdelete']=1

                if adminapkupload==1:
                    adminapkupload=0
                    params['adminapkupload']=1

                if incorrectfile==1:
                    incorrectfile=0
                    params['incorrect']=1

                if canupdatecollisions==1:
                    canupdatecollisions=0
                    params['canupdate']=1

                if canupdatecollisions==3:
                    canupdatecollisions=0
                    params['canupdate1']=1

                if canupdatecollisions==2:
                    print "inside here"
                    canupdatecollisions=0
                    cur.execute("SELECT resource from apks1 WHERE package_name='"+apktoupdate+"' AND version='"+apktoupdateversion+"'")
                    con.commit()
                    z=cur.fetchall();

                    x=z[0]['resource'].split(',')
                    print "resources are",x
                    xx=[]
                    cur.execute("SELECT resource_name from coll1 ")
                    con.commit()
                    r=cur.fetchall();

                    for i in range(len(x)):
                        for j in range(len(r)):
                            if x[i]==r[j]['resource_name']:
                                xx.append(x[i])

                    xxx=list(set(x) - set(xx))

                    print "xxx ix",xxx
                    params['updateresource']=xxx


                logintime=session['logintime']

                return render_template('admin.html',param=params,log=logintime)

            return redirect(url_for('mainpage'))

        else:
            return redirect(url_for('mainpage'))

#################################################################################

@app.route('/login',methods=['POST','GET'])               #Endpoint for Login (To authenticate users)
def login():
    global developername
    global coll
    global times
    global names
    global collflag
    global aaa
    global fail
    global con
    global cur
    
                                                       #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    
    
    coll={}
    times=""
    names=""
    collflag=0

    if request.method=='POST':                                                     #Get loginid and password from user
 
        aaa=request.form['logins']
        b=md5.md5(str(request.form['passwords'])).hexdigest()

        cur.execute("SELECT loginid,password FROM developer1 WHERE loginid='"+aaa+"' and password='"+b+"'")
        con.commit()

        c=cur.fetchall()
        print c

        if len(c)<1:
            fail=1
            return redirect(url_for('logout'))
        else:
            cur.execute("SELECT logintime from developer1 WHERE loginid='"+aaa+"'")
            con.commit()
            logintime=cur.fetchall()

            if aaa=='admin':                                                         #Admin Login
                fail=0
                session['username']=aaa
                session['logintime']=logintime
                return redirect(url_for('admin'))

            else:                                                                    #Developer Login
                fail=0
                cur.execute("SELECT developer_name FROM developer1 WHERE loginid='"+aaa+"'")
                con.commit()
                developername=cur.fetchall()


                session['username']=aaa
                session['logintime']=logintime
                return redirect(url_for('developer'))


#################################################################################

@app.route('/account',methods=['POST','GET'])                     #Endpoint for creating and deleting accounts and developers
def account():
    flag=0
    global coll
    global times
    global names
    global collflag
    global accountexist
    global accountnotexist
    global developerexist
    global developernotexist
    global saveadmin
    global invalidinput
    global incorrectfile
    global accountcreate
    global accountdelete
    global developeradd
    global developerdelete
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()


    coll={}
    times=""
    names=""
    collflag=0

    if request.method=='POST':

        if 'username' in session:

            try:
                b=request.form['newaccountname']                                   #Get uploaded keystore file,account name in case 
                k=request.files['keystorefile']                                    #of new account 
                flag=1
                print 'keystore'
                print k.filename
                print flag
            except:
                try:                                                              #Get name of account to be deleted
                    b=request.form['accountname']
                    flag=2
                except:
                    try:
                        b=request.form['newdeveloper']                            #Get name of developer to be added
                        flag=3
                    except:
                        try:
                            b=request.form['developer']                           #Get name/loginid of developer to be removed
                            bb=request.form['developer2']
                            flag=4
                        except:
                            pass

            if flag==1 or flag==2:

                cur.execute("SELECT *  FROM account1 WHERE account_name='"+b+"'")
                con.commit()
                t=cur.fetchall()

                if flag==1:
                    if b=="":
                        invalidinput=1
                        return redirect(url_for('admin'))
                    elif not k:
                        incorrectfile=1
                        return redirect(url_for('admin'))

                    elif len(t)==1:
                        accountexist=1
                        return redirect(url_for('admin'))

                    else:
                        check1=str(secure_filename(k.filename)).rfind('.')
                        check=str(secure_filename(k.filename))[check1+1:]

                        if check!='keystore':                                             #Check if keystore file has  
                            incorrectfile=1                                               #extension .keystore  
                            return redirect(url_for('admin'))
                        else:
                            keyname=secure_filename(k.filename)                             
                            k.save('./keystore/' + b+'_'+keyname)                          #Save keystore file
                            subprocess.call("sudo chmod -R 777 ./keystore",shell=True)
                            accountcreate=1
                            aa = "INSERT INTO account1 (account_name,keystorefile) VALUES ('"+b+"','"+keyname+"')"
                            cur.execute(aa)
                            con.commit()
                            return redirect(url_for('admin'))

                if flag==2:
                    if len(t)<1:
                        accountnotexist=1
                        return redirect(url_for('admin'))

                    else:
                        accountdelete=1
                        aa = "DELETE FROM account1 WHERE account_name='"+b+"'"
                        cur.execute(aa)
                        con.commit()
                        return redirect(url_for('admin'))

            if flag==3 or flag==4:

                if len(b)>0:
                    if len(b.split(" "))>1:
                        f=b.split(" ")[0].lower()
                        l=b.split(" ")[1].lower()
                        login=f+"."+l

                    if len(b.split(" "))==1:
                        f=b.split(" ")[0].lower()
                        login=f

                elif flag==4 and len(bb)>0:
                    login=bb

                else:
                    login=""

                cur.execute("SELECT * FROM developer1 WHERE loginid='"+login+"'")
                con.commit()
                t=cur.fetchall()

                if flag==3:
                    if login=="":
                        invalidinput=1
                        return redirect(url_for('admin'))

                    if len(t)==1:
                        developerexist=1
                        return redirect(url_for('admin'))
                    else:
                        developeradd=1
                        passw=md5.md5(f).hexdigest()
                        aa = "INSERT INTO developer1 (developer_name,loginid,password) VALUES ('"+b+"' ,'"+login+"' ,'"+passw+"' )"
                        cur.execute(aa)
                        con.commit()
                        return redirect(url_for('admin'))

                if flag==4:
                    if login=="":
                        invalidinput=1
                        return redirect(url_for('admin'))

                    elif len(t)<1:
                        developernotexist=1
                        return redirect(url_for('admin'))
                    elif login=="admin":
                        saveadmin=1
                        return redirect(url_for('admin'))
                    else:
                        developerdelete=1
                        aa = "DELETE FROM developer1 WHERE loginid='"+login+"'"
                        cur.execute(aa)
                        con.commit()
                        return redirect(url_for('admin'))

        else:
            return redirect(url_for('logout'))


    else:
         if 'username' in session:
             return render_template('admin.html')
         else:
             return redirect(url_for('logout'))


#################################################################################

@app.route('/developer')                              #Endpoint for Developer Page
def developer():
    global developername
    global coll
    global names
    global times
    global collflag
    global incorrectfile
    global uploadsuccess
    global testsuccess
    global passchange
    global aaa
    global canupdatecollisions
    global apktoupdate
    global apktoupdateversion
    global xxx
    global changelogempty
    global emailfrom
    global emaildomain1
    global con
    global cur
    
                                                #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    if 'username' in session:

        cur.execute("SELECT account_name FROM account1")
        con.commit()
        a=cur.fetchall()

        print developername
        develop=session['username']

        az="SELECT package_name,account_name,version,apk_name from apks1 WHERE loginid='"+aaa+"'"
        cur.execute(az)
        con.commit()
        uploaddata=cur.fetchall()

        print "length:" ,len(uploaddata),uploaddata
        params={}
        params['accountnames']=a
        params['Developer']=develop
        #params['Developer']=develop[0]['developer_name']
        params['apkname']=names
        params['duration']=times

        if incorrectfile==1:                                 #Print "Incorrect File Type"
            incorrectfile=0
            params['incorrect']=1

        if len(uploaddata)<1:
            params['udata']="NO UPLOADED APKS"
        if len(uploaddata)>=1:
            params['udata1']=uploaddata

        if uploadsuccess==1:                                #Print "Package Successfully Uploaded"
            uploadsuccess=0
            params['uploadsucess1']=1

        if uploadsuccess==2:                                #Print "APK Version Already Exists"
            uploadsuccess=0
            params['uploadsucess2']=1

        if testsuccess==1:                                  #Print "Package Successfully Tested"
            testsuccess=0
            params['testsucess']=1

        if passchange==1:                                   #Print "Incorrect Password ! Try Again!!"
            passchange=0
            params['passchange1']=1

        if passchange==2:                                   #Print "Passwords Do Not Match ! Try again !!"
            passchange=0
            params['passchange2']=1

        if passchange==3:                                   #Print  "Passwords Changed Successfully"
            passchange=0
            params['passchange3']=1

        if emailfrom==1:                                    #Print "Email Field is Empty"
            emailfrom=0
            params['emailfrom']=1

        if emailfrom==2:                                   #Print "Email Couild Not be Sent"
            emailfrom=0
            params['emailfrom1']=1

        if emailfrom==3:                                   
            emailfrom=0
            if emaildomain1=='xyz.com':
                data='http://google.xyz.com'
                params['emaildomain']=json.dumps(data)
            else:
                data='http://www.'+emaildomain1
                print data
                data='http://www.gmail.com'
                params['emaildomain']=json.dumps(data)
            params['emailfrom2']=1

        if emailfrom==4:                                  #Print "Email was not Verified!" 
            emailfrom=0
            params['emailfrom3']=1

        if changelogempty==1:                             #Print "ChangeLog is Empty !"
            changelogempty=0
            params['changelogempty']=1

        if changelogempty==2:                            #Print "Email sent Successfully"
            changelogempty=0
            params['changelogempty1']=1


        if canupdatecollisions==1:                       #Print "Cannot Update Collisions!" 
            canupdatecollisions=0
            params['canupdate']=1

        if canupdatecollisions==3:                       #Print "Collisions Updated !"
            canupdatecollisions=0
            params['canupdate1']=1

        if canupdatecollisions==2:
            canupdatecollisions=0
            cur.execute("SELECT resource from apks1 WHERE package_name='"+apktoupdate+"' AND version='"+apktoupdateversion+"'")
            con.commit()
            z=cur.fetchall();

            x=z[0]['resource'].split(',')
            print "resources are",x
            xx=[]
            cur.execute("SELECT resource_name from coll1 ")
            con.commit()
            r=cur.fetchall();

            for i in range(len(x)):
                for j in range(len(r)):
                    if x[i]==r[j]['resource_name']:
                        xx.append(x[i])

            xxx=list(set(x) - set(xx))

            params['updateresource']=xxx

        logintime=session['logintime']

        if collflag==0:

                params['collstatus']="NO APKS TO TEST"
                return render_template('developer.html',param=params,log=logintime)

        elif collflag==1:

                params['collstatus1']="NO COLLISIONS"
                return render_template('developer.html',param=params,log=logintime)

        elif collflag==2:

                params['collstatus']="NO COLLISIONS"
                return render_template('developer.html',param=params,log=logintime)

        else:

                for i in coll.keys():
                    coll[i]['clash']=[]
                    coll[i]['notclash']=[]

                    if len(coll[i]['importance'])==0:
                        coll[i]['clash'].append("No clashes")
                        coll[i]['notclash'].append("No clashes")

                    for j in range(len(coll[i]['importance'])):
                        if coll[i]['importance'][j]=='R':
                            coll[i]['clash'].append(coll[i]['resources'][j])
                        else:
                            coll[i]['notclash'].append(coll[i]['resources'][j])


                for i in coll.items():
                    print i[0]

                print coll

                params['collisions']=coll
                return render_template('developer.html',param=params,log=logintime)

    else:
        return redirect(url_for('mainpage'))

#################################################################################

@app.route('/upload',methods=['POST','GET'])                #Endpoint for uploading apks
def upload():
    global coll 
    global times
    global names
    global collflag
    global aa
    global aaa
    global cc
    global sha
    global resource
    global incorrectfile
    global testsuccess
    global version
    global adminapkupload
    global developername
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    if 'username' in session:

        collflag=0
        count=0
        if request.method=='POST':
            b=request.files['testapk']                                            #Get Uploaded APK and account
            cc=request.form['acc']

            if not b:
                incorrectfile=1
                return redirect(url_for('developer'))
            else:
                check1=str(secure_filename(b.filename)).rfind('.')                              
                check=str(secure_filename(b.filename))[check1+1:]
                if check!='apk':                                                     #Check if APK has extension .apk
                    incorrectfile=1
                    return redirect(url_for('developer'))
                else:
                    b.save('./apks/' + secure_filename(b.filename))                  #Save APK file
                    subprocess.call("sudo chmod -R 777 ./apks",shell=True)

            name=secure_filename(b.filename)
            names=name
            z=zipfile.ZipFile('./apks/'+name)

            v=" ./apks/"+name
            w=" ./apks/out"

            subprocess.call("sudo chmod -R 777 ./apks",shell=True)
            try:
                subprocess.call("sudo apktool d -f ./apks/%s ./apks/out  "%name ,shell=True)           #Get AndroidManifest.xml using
            except:                                                                                    #apktool in /apks/out
                subprocess.call("sudo apktool d -f ./apks/%s ./apks/out -f "%name ,shell=True)

            subprocess.call("sudo chmod -R 777 ./apks",shell=True)
            for f in z.namelist():                                                                     #Extract MANIFEST.MF file from apk
                if f=='META-INF/MANIFEST.MF':
                    z.extract(f,'./apks')
                    subprocess.call("sudo chmod -R 777 ./apks",shell=True)

            gg=open("./apks/out/AndroidManifest.xml",'r').read()
            v1=gg.find('versionName=')+13
            v2=gg.find('package=')+9
            aa=str(gg[v2:gg.find('"',v2)])
            version=str(gg[v1:gg.find('"',v1)])                                                       #Get version of APK


            apkname=name.rfind('.')
            apkname1=name[apkname+1:]
            apkname2=name[:apkname]

            subprocess.call(" sudo mv ./apks/%s ./apks/%s"%(name,apkname2+version+"."+apkname1),shell=True)    #Rename apk->apknameversion.apk



            a=open('./apks/META-INF/MANIFEST.MF',"r")
            b=[];c=[];
            i=0
            for line in a:
                if len(line.split('SHA1-Digest: '))==2:
                    b.append(line.split('SHA1-Digest :'))
                    b[i]=str(b[i]).split('SHA1-Digest: ')[1].split('\\r')[0]
                    i=i+1
                if len(line.split('Name: '))==2:
                    c.append(line.split('Name :'))
                    c[i]=str(c[i]).split('Name: ')[1].split('\\')[0]

            sha=""
            resource=""

            for i in range(len(b)-1):                                                     #Get names and sha1's of resources in MANIFEST.MF
                sha=sha+str(b[i])+","
                resource=resource+str(c[i])+","
            sha=sha+str(b[len(b)-1])
            resource=resource+str(c[len(c)-1])

            if aaa=='admin':
                aa = "INSERT INTO apks1 (package_name,apk_name,account_name,sha1s,resource,time,loginid,version) VALUES ('"+aa+"','"+names+ "' ,'" +cc+"' , '" + sha + "', '"+resource+"', '"+str(datetime.datetime.now())+"','"+aaa+"' , '"+version+"')"
                cur.execute(aa)
                con.commit()
                adminapkupload=1
                return redirect(url_for('admin'))


            cur.execute("SELECT sha1s,resource,account_name from apks1 ")
            con.commit()
            a=cur.fetchall()


            if len(a)<1:                                                                 #If not apks uploaded ,simply insert it
                aa = "INSERT INTO apks1 (package_name,apk_name,account_name,sha1s,resource,time,loginid,version) VALUES ('"+aa+"','"+names+ "' ,'" +cc+"' , '" + sha + "', '"+resource+"', '"+str(datetime.datetime.now())+"','"+aaa+"' , '"+version+"')"
                cur.execute(aa)
                con.commit()
                collflag=2

                testsuccess=1
                return redirect(url_for('developer'))

            else:                                                                        #Prepare a collsion list -important
                                                                                         #and unimportant according to accounts
                #cur.execute("SELECT DISTINCT account_name from apks1 ")
                #con.commit()
                #d=cur.fetchall()

                coll={}

                print "uploaded sha",b
                print "uploaded  resources",c

                for i in range(len(a)):
                    x=a[i]['sha1s'].split(',')
                    y=a[i]['resource'].split(',')


                    t=list(set(x)&set(b))

                    print "Dert",t

                    colls={}
                    colls['resources']=[]
                    count1=0
                    for l in range(len(x)):
                        for j in range(len(b)):
                            if b[j]==x[l]:
                                colls['resources'].append(y[l])
                                count1=count1+1
                            '''
                            try:
                                #coll[a[i]['account_name']]=coll[a[i]['account_name']]+a[i]['resource']
                                colls['resource'].append(y[i])
                                count=count+1
                                print coll
                            except:
                                coll[a[i]['account_name']]['resource']=y[i]
                                #coll[a[i]['account_name']]=a[i]['resource']
                                print coll
                                count=count+1
                             '''

                    print "realcol",colls


                    if a[i]['account_name'] in coll.keys():
                        for k in colls['resources']:
                            coll[a[i]['account_name']]['resources'].append(k)

                    else:
                        coll[a[i]['account_name']]=colls



                print count1

                cur.execute("SELECT resource_name from coll1")
                con.commit()
                safe=cur.fetchall()

                for i in coll.keys():
                    coll[i]['importance']=[]

                for i in coll.keys():
                    for j in range(len(coll[i]['resources'])):
                        coll[i]['importance'].append("p")
                        for k in safe:
                            if k['resource_name']==coll[i]['resources'][j]:
                                print coll[i]['resources'][j]
                                if coll[i]['importance'][j]=="p":
                                    coll[i]['importance'][j]="G"


                for i in coll.keys():
                    for j in range(len(coll[i]['resources'])):
                        if coll[i]['importance'][j]=="p":
                            coll[i]['importance'][j]="R"

                #print coll

                times=str(datetime.datetime.now())

                    #print "collisions are" ,coll

                if coll=={}:
                    collflag=1
                else:
                    collflag=3

                testsuccess=1
                return redirect(url_for('developer'))
    else:
        return redirect(url_for('mainpage'))

#################################################################################
@app.route('/showupload',methods=['POST','GET'])                 #Endpoint for uploading (contd.)
def showupload():

    global cc
    global sha
    global resource
    global collflag
    global aa
    global aaa
    global uploadsuccess
    global version
    global developername
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    if request.method=='POST':

        if 'username' in session:


            a="SELECT package_name from apks1 WHERE package_name='"+aa+"'AND version='"+version+"'AND loginid='"+aaa+"'"
            print a
            cur.execute(a)
            con.commit()
            a=cur.fetchall()
            print len(a)

            if len(a)<1:
                print 'inside1'
                aba = "INSERT INTO apks1 (package_name,apk_name,account_name,sha1s,resource,time,loginid,version) VALUES ('"+aa+"','"+names+ "' ,'" +cc+"' , '" + sha + "', '"+resource+"', '"+str(datetime.datetime.now())+"','"+aaa+"','"+version+"')"
                cur.execute(aba)
                con.commit()
                collflag=0;
                uploadsuccess=1
                return redirect(url_for('developer'))

            else:
                collflag=0;
                uploadsuccess=2
                return redirect(url_for('developer'))

        else:
            return redirect(url_for('mainpage'))

#################################################################################
@app.route('/logout')                                           #Endpoint for logout
def logout():
    global aaa
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    cur.execute("UPDATE developer1 SET logintime='"+str(datetime.datetime.now())+"' WHERE loginid='"+aaa+"'")
    con.commit()
    session.pop('username', None)
    session.pop('logintime',None)
    return redirect(url_for('mainpage'))

#################################################################################

@app.route('/changepass',methods=['POST','GET'])                #Endpoint to change password
def changepass():
    global aaa
    global passchange
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    if request.method=='POST':

        if 'username' in session:


            neww=request.form['newpass']
            renew=request.form['renewpass']

            old=md5.md5(str(request.form['oldpass'])).hexdigest()

            cur.execute("SELECT password from developer1 WHERE password='"+old+"'")
            con.commit()
            old=cur.fetchall()

            if len(old)<1:
                passchange=1
                return redirect(url_for('developer'))

            if len(old)==1:
                if neww!=renew:
                    passchange=2
                    return redirect(url_for('developer'))
                if neww==renew:
                    passchange=3
                    neww=md5.md5(neww).hexdigest()
                    cur.execute("UPDATE developer1 SET password='"+neww+"' WHERE loginid='"+aaa+"'")
                    con.commit()
                    return redirect(url_for('developer'))
        else:
            return redirect(url_for('logout'))

#################################################################################

@app.route('/updatecollision',methods=['POST','GET'])             #Endpoint to update collisions
def updatecollision():
    global aaa
    global canupdatecollisions
    global apktoupdateversion
    global apktoupdate
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    if request.method=='POST':

        if 'username' in session:
            flag=0
            apktoupdate=request.form['updateapkcollisions']
            apktoupdateversion=request.form['updateapkcollisionsversion']


            if aaa=="admin":

                cur.execute("SELECT package_name,account_name,apk_name,version,time,developer_name FROM apks1,developer1 WHERE apks1.loginid=developer1.loginid ")
                con.commit()
                apk=cur.fetchall()

            else:

                cur.execute("SELECT package_name,account_name,apk_name,version,time,developer_name FROM apks1,developer1 WHERE apks1.loginid=developer1.loginid AND developer1.loginid='"+aaa+"'")
                con.commit()
                apk=cur.fetchall()

            print apk

            for i in range(len(apk)):
                if apk[i]['package_name']==apktoupdate and apk[i]['version']==apktoupdateversion:
                    flag=1

            if  flag==1:
                canupdatecollisions=2
                print "can update"
                if aaa=="admin":
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('developer'))

            else:
                canupdatecollisions=1
                print "cannot update"
                if aaa=="admin":
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('developer'))

        else:
            return redirect(url_for('logout'))


#################################################################################

@app.route('/update',methods=['POST','GET'])                         #Endpoint to update collisions (contd.)
def update():
    global xxx
    global aaa
    global canupdatecollisions
    global con
    global cur
    
                                                #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    
    if request.method=='POST':
        collisionlist=[]

        if 'username' in session:

            print "xxx" ,xxx


            print request.form.keys()

            for i in request.form.keys():
                if i in xxx:
                    collisionlist.append(i)

            print "collsionlist is ",collisionlist
            for i in collisionlist:
                try:
                    cur.execute("INSERT INTO coll1 (resource_name) VALUES('"+i+"')")
                    con.commit();
                except:
                    pass

            canupdatecollisions=3
            if aaa=="admin":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('developer'))


        else:
            return redirect(url_for('logout'))

#################################################################################


@app.route('/sendemail',methods=['POST','GET'])                       #Endpoint to send email
def sendemail():
    global aaa
    global changelogempty
    global emailfrom
    global connection
    global askemail
    global emaildomain1
    global msg
    global con
    global cur
    
                                                 #To check if database connection is intact 

    con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

    cur = con.cursor()

    if request.method=='POST':

        if 'username' in session:                                   #Get email address ,apkversion and changelog
            emailoption=request.form['sendemail']
            changelog=request.form['changelog']
            askemail=request.form['askemail']

            emailoption=emailoption.split('#')
            emailapk=str(emailoption[0])
            emailversion=str(emailoption[1])

            print emailapk
            print emailversion
            print changelog

            if len(askemail)<1:
                emailfrom=1
                print 'Length is <1'
                return redirect(url_for('developer'))


            elif len(changelog)<1:
                  changelogempty=1
                  print 'Length is <1'
                  return redirect(url_for('developer'))

            else:

                az="SELECT apks1.account_name,keystorefile from apks1,account1 WHERE loginid='"+aaa+"' AND apk_name='"+emailapk+"' AND         version='"+emailversion+"' AND apks1.account_name=account1.account_name"
                cur.execute(az)
                con.commit()
                azz=cur.fetchall()

                apkname=emailapk.rfind('.')
                apkname1=emailapk[apkname+1:]
                apkname2=emailapk[:apkname]

                attachapk=apkname2+emailversion+"."+apkname1
                attachkeystore=str(azz[0]['account_name'])+"_"+str(azz[0]['keystorefile'])

                mimeattachapk=apkname2+emailversion+"."

                keystorename=attachkeystore.rfind('.')
                keystorename1=attachkeystore[:keystorename]

                mimeattachkeystore=keystorename1+"."

                print attachapk
                print attachkeystore


                msg = MIMEMultipart()
                msg['Subject'] = apkname2+'_'+emailversion+'_'+'ReleaseMail'
                msg['From'] = askemail                                            #Developer's Email is Sender's EMail
                msg['To'] = 'email@gmail.com'                        #Receiver Email is fixed

                msg.preamble = 'Multipart message.\n'

                part = MIMEText(changelog)
                msg.attach(part)

                part = MIMEApplication(open('./apks/'+attachapk, 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename=mimeattachapk+'zip')
                msg.attach(part)                                                 #Attach .apk with filename as .zip , need to rename it to
                                                                                 #.apk when it is downloaded
                part = MIMEApplication(open('./keystore/'+attachkeystore, 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename=mimeattachkeystore+'txt')
                msg.attach(part)                                                 #Attach .keystore with filename as .txt , need to rename it to
                                                                                 #.keystore when it is downloaded 
                try:
                    connection = boto.connect_ses(aws_access_key_id='aws access key id'
                                              , aws_secret_access_key='aws secret access key')

                    connection.verify_email_address(askemail)                   #Send an email from AmazonSES for mail verification  
                    emailfrom=3

                    emaildomain=askemail.rfind('@')
                    emaildomain1=askemail[emaildomain+1:]

                    return redirect(url_for('developer'))

                except:
                       emailfrom=2
                       return redirect(url_for('developer'))

        else:
            return redirect(url_for('logout'))

#################################################################################

@app.route('/verifyemail',methods=['POST','GET'])               #Endpoint to send email (contd.)
def verifymail():

     global connection
     global askemail
     global emailfrom
     global changelogempty
     global msg
     global con
     global cur
    
                                                  #To check if database connection is intact 

     con=mdb.connect( host='localhost', user='loginname',
     passwd='password', db='databasename',
     cursorclass=MySQLdb.cursors.DictCursor)

     cur = con.cursor()

     if request.method=='POST':

              if 'username' in session:


                    confirmed=connection.list_verified_email_addresses()          #Get list of verified email addresses from Amazon SES
                    confirmed1=confirmed['ListVerifiedEmailAddressesResponse']['ListVerifiedEmailAddressesResult']['VerifiedEmailAddresses']

                    if askemail not in confirmed1:
                        emailfrom=4
                        return redirect(url_for('developer'))
                    try:
                        result = connection.send_raw_email(msg.as_string()        #Send Email
                                                   , source=msg['From']
                                                  , destinations=[msg['To']])
                        print result

                    except:
                        emailfrom=2
                        return redirect(url_for('developer'))


                    connection.delete_verified_email_address(askemail)           #Remove email address of developer from list of verified mails
                    changelogempty=2
                    return redirect(url_for('developer'))
              else:
                  return redirect(url_for('logout'))

#################################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)                               #Run the whole program
