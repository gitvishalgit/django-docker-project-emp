from django.shortcuts import render,redirect
from django.conf import settings
from django.core.mail import send_mail
from django.db import connection
from django.contrib.auth.hashers import make_password,check_password
from datetime import *
from .config import key
from cryptography.fernet import Fernet

f = Fernet(key)
mycursor = connection.cursor()



def login(request):
    """
        Desc:
            1: Accepts the username and password and authenticate it.
        para:
            1: request
        return:
            1: returns to the homepage(Shows all Records related to the loggedin user) 
        Error:
            1: if username and passwords are invalid then invalid msg will displayed

    """

    if 'emailid' not in request.session:
        if request.method =='POST':
            password=request.POST['password']
            emailid=request.POST['emailid']
            try:
                mycursor.execute('select * from register where emailid = "%s"'%(request.POST['emailid']))
                data = mycursor.fetchone()
            except:
                data=None
            if data is not None:
                if check_password(password, data[5]):
                    request.session['emailid'] = emailid
                    msg = emailid.encode()
                    token = f.encrypt(msg).decode()
                    return redirect(homepage,token=token)
                else:
                    return render(request,'login.html',{'message':'Incorrect Password'})
            else:
                return render(request,'login.html',{'message':'Incorrect UserName And Pasword'})
        else:
            return render(request,'login.html')
    else:
        emailid = request.session['emailid']
        msg = emailid.encode()
        token = f.encrypt(msg).decode()
        return redirect(homepage,token=token)

def logout(request):
    """
        Desc:
            1: logout's the user and deletes the session
        para:
            1: request
        return:
            1: returns to the login page
    """
    del request.session['emailid'] 
    return redirect(login)


def homepage(request,token):
    '''
        Desc:
            1: Shows the records of the logged-in user
        para:
            1: request
            2: token(token is encrypted and decoded emailid of loggedin user)(dtype: str)
        return:
            1: returns the loggedin.html page where all data and related actions(Add,Update,Delete) where given
    ''' 

    if 'emailid' in request.session:
        token_bytes=token.encode()
        final_token = f.decrypt(token_bytes)
        emailid = final_token.decode()   
        mycursor.execute('select * from register where emailid = "%s"'%(emailid))
        user = mycursor.fetchone()

        mycursor.execute('select * from Employee where useremail = "%s"'%(emailid))
        data = mycursor.fetchall()

        if len(data)!=0:
            return render(request,'logged_in.html',{'data':data,'name':user[1],'token':token})
        else:
            return render(request,'logged_in.html',{'message':'Record Not Found!!!','name':user[1],'token':token})
    else:
        return redirect(login)

def add_employee(request,token):
    '''
        Desc:
            1: This View will called when the Add Employee button is clicked.
            2: Once Post request is called, All data is grabbed from Html and saved to Employee table.
        para:
            1: request
            2: token(token is encrypted and decoded emailid of loggedin user)(dtype: str)
        return:
            1: returns to the same page for adding more employees
            2: For Homepage, please click Back to Home
    ''' 
    if 'emailid' in request.session:
        token_bytes=token.encode()
        final_token = f.decrypt(token_bytes)
        emailid = final_token.decode()  
        if request.method == 'POST':
            fname = request.POST['First_Name']
            lname = request.POST['Last_Name']
            DOB = request.POST['DOB']
            gender = request.POST['gender']
            department = request.POST['department']
            position = request.POST['position']
            Eemailid = request.POST['emailid']
            password = request.POST['password']

            mycursor.execute('insert into Employee(First_Name,Last_Name,gender,emailid,password,DOB,department,position,useremail) \
                                    values("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(fname,lname,gender,Eemailid,password,
                                                                        DOB,department,position,emailid))
            connection.commit()
            return redirect(homepage,token=token)
        else:   
            return render(request,'add_student.html',{'token':token})
    else:
        return redirect(login)


def forget(request):
    '''
        Desc:
            1: This View will called when the forgot password is clicked.(from login page)
            2: Takes the Emailid and Sends Email with the password updation link where link consists of TOKEN
               here,
                    TOKEN : Token is a hash of emailid(created from make_password)
            3: TOKEN and the requested time is saved in Database(Employee table)
        para:
            1: request
        return:
            1: returns to the Page(done.html) With back to login link
    '''
    if request.method=='POST':
        try:
            mycursor.execute(' select * from register where emailid ="%s" '%(request.POST['email']))
            x = mycursor.fetchone()
        except:
            x=None
        print(x)
        if x is None:
            return render(request,'done.html',{'message':'Email Id is not registered'})
        elif x[-1] is not None:
            return render(request,'done.html',{'message':'You have already requested, please check email'})
        else:
            token = make_password(x[4])
            while '/' in token:
                token = make_password(x[4])
            subject = 'Forget Password'
            message = f'hi click this http://127.0.0.1:8000/passwordchange/{token}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [x[4]]
            mycursor.execute('update register set req_time = now(),token = "%s" where emailid = "%s"'%(token,x[4]))
            connection.commit()
            send_mail(subject,message,email_from,recipient_list)
            return render(request,'done.html',{'message':'Email has been sent'})
    else:
        return render(request,'forget.html')
    

def update_password(request,token):
    """
        Desc:
            1: This View will called when the link sent via email is opened
            2: This link is valid only till 10 mins or until the password updations
        para:
            1: request
            2: token(it is a hashed email which is sent)
        return:
            1: returns to the Page(done.html) With back to login link
        errors:
            1: if passwords are not identical shows the msg on the same page
    """
    mycursor.execute('select emailid,req_time from register where token = "%s"'%token)
    data = mycursor.fetchone()
    if data is None:
        return render(request,'done.html',{'message':'Link has been expired'})
    else:
        emailid = data[0]
        req_time = data[1]
        diffrence = datetime.now()-req_time
        if diffrence.total_seconds()/60 < 10 :
            if request.method == 'POST':
                mycursor.execute(' select * from register where emailid ="%s" '%(emailid))
                x = mycursor.fetchone()
                pass1 = request.POST['password1']
                pass2 = request.POST['password2']
                if pass1 == pass2:
                    mycursor.execute('update register set password="%s",token=null,req_time=null where emailid = "%s"'%(make_password(pass1),emailid))
                    connection.commit()
                    return render(request,'done.html',{'message':'Password Updated Successfully!!!'})
                else:
                    return render(request,'update_password.html',{'data':x[1],'message':'Passwords are not Identical.'})
            else:
                mycursor.execute('select * from register where emailid ="%s"'%(emailid))
                x = mycursor.fetchone()
                return render(request,'update_password.html',{'data':x[1]})
        else:
            mycursor.execute('update register set token=null,req_time=null where emailid = "%s"'%(emailid))
            connection.commit()
            return render(request,'done.html',{'message':'Link has been expired'})

    
    

def register(request):
    """
        Desc:
            1: This view is called when the Sign in Clicked
            2: New registration occurs and Data is saved th database(register table)
        para:
            1: request
        return:
            1: returns to the done.html with msg of registration
        errors:
            1: if email is already registered it will show error
    """
    if request.method == 'POST':
        try:
            mycursor.execute('select * from register where emailid ="%s"'%(request.POST['emailid']))
            x = mycursor.fetchone()
        except:
            x=None
        print(x)
        if x is None:
            mycursor.execute('insert into register(First_Name,Last_Name,gender,emailid,password) \
                                values("%s","%s","%s","%s","%s")'%(request.POST['First_Name'],
                                                                    request.POST['Last_Name'],
                                                                    request.POST['gender'],
                                                                    request.POST['emailid'],
                                                                    make_password(request.POST['password']) 
                                                                    ))
            connection.commit()
            return render(request,'done.html',{'message':'Registration successfull'})
        else:
            return render(request,'register.html',{'message2':'email id already register exists.'})
    else:
        return render(request,'register.html')
    

        
def update(request,token):
    """
        Desc:
            1: This view is called when update is clicked for the particular employee
            2: updates the requested record and saves the changes in database
        para:
            1: request
            2: token(token is encrypted and decoded emailid of loggedin user)(dtype: str)
            3: eid(the Employee id for which update request is called)
        redirect:
            1: redirects to the Homepage For Showing updations
    """
    if 'emailid' in request.session:
        if request.method == 'POST':
            id = request.POST['userid']
            mycursor.execute('select *  from Employee where id = %d'%int(id))
            data = mycursor.fetchone()
            fname = request.POST['First_Name']
            lname = request.POST['Last_Name']
            DOB = request.POST['DOB']
            gender = request.POST['gender2']
            department = request.POST['department2']
            position = request.POST['position2']
            Eemailid = request.POST['emailid']
            mycursor.execute('update Employee set First_Name="%s",Last_Name="%s",gender="%s",emailid="%s",DOB="%s",department="%s",position="%s" where id=%d\
                                    '%(fname,lname,gender,Eemailid,DOB,department,position,int(id)))
            connection.commit()
            return redirect(homepage,token=token)
    else:
        return redirect(login)


def delete(request,token):
    """
        Desc:
            1: This view is called when delete is clicked for the particular employee
            2: deletes the requested record and saves the changes in database
        para:
            1: request
            2: token(token is encrypted and decoded emailid of loggedin user)(dtype: str)
            3: eid(the Employee id for which delete request is called)
        redirect:
            1: redirects to the Homepage For Showing deletions
    """
    if 'emailid' in request.session:
        if request.method == 'POST':
            eid = request.POST['id']
            print(eid)
            mycursor.execute('delete from Employee where id = %d'%int(eid))
            connection.commit()
            return redirect(homepage,token=token)
        else:
            return redirect(homepage,token=token)
    else:
        return redirect(login)


