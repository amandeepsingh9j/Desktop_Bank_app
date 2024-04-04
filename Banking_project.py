#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#**************Database Query***********************************

try:
    import sqlite3
    con=sqlite3.connect(database='bank.sqlite')
    cur=con.cursor()
    cur.execute("create table account(acn integer primary key autoincrement,password text,name text,mob text,email text,balance float,date text)")
    cur.execute("create table txn(acn int,type text,amt float,updatedbal float,date text)")
    con.commit()
    con.close()
    print("Table created")
except Exception as e:
    print(e)


#**************************Project dependencies module**************


from tkinter import *
import time
import re
import os
import shutil
from PIL import Image,ImageTk
from tkinter import messagebox,filedialog
from tkinter.scrolledtext import Scrollbar,ScrolledText




#***************Project Code***********************************



win=Tk()
win.state("zoomed")
win.configure(bg='powder blue')


font=('arial',20,'bold')
bg='pink'


lbl=Label(win,text="Banking Project",font=('arial',20,'bold','underline'),bg='powder blue')
lbl.pack()



def login_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    
    # title=Label(frm,text="Welcome User",font=('arial',15,'bold','underline'),bg='pink')
    # title.pack()
    
    
    def reset():
        entry_acn.delete('0',END)
        entry_pass.delete('0',END)
        entry_acn.focus()
        
    def open_new_acn():
        frm.destroy()
        new_screen()
        
    def forget():
        frm.destroy()
        forget_screen()
        
    def login():
        acn=entry_acn.get()
        pwd=entry_pass.get()
        if (len(acn)==0 or len(pwd)==0):
            messagebox.showerror("Failed",'Invalid Account Number & Password')
            return
        import sqlite3
        con=sqlite3.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute('select * from account where acn=? and password=?',(acn,pwd))
        global tup
        tup=cur.fetchone()
        if tup==None:
            messagebox.showerror("Login Failed",'Invalid Account Number & Password')
            return
        
        else:
            frm.destroy()
            welcome_screen()
    
    lbl_acn=Label(frm,text="Account Number:",font=font,bg=bg)
    lbl_acn.place(relx=0.2,rely=0.2)
    
    entry_acn=Entry(frm,font=font,bd=3,width=25)
    entry_acn.place(relx=0.45,rely=0.2)
    
    lbl_pass=Label(frm,text="Password:",font=font,bg=bg)
    lbl_pass.place(relx=0.2,rely=0.3)
    
    entry_pass=Entry(frm,font=font,bd=3,width=25,show="*")
    entry_pass.place(relx=0.45,rely=0.3)
    
    btnlogin=Button(frm,text="Login",font=font,bg='white',width=10,command=login)
    btnlogin.place(relx=0.28,rely=0.47)
    
    btnreset=Button(frm,text="Reset",font=font,bg='white',width=10,command=reset)
    btnreset.place(relx=0.443,rely=0.47)
    
    btnnewacn=Button(frm,text="Open New Account",font=font,bg='white',width=25,command=open_new_acn)
    btnnewacn.place(relx=0.28,rely=0.6)
    
    btnforget=Button(frm,text="Forgot Password",font=font,bg='white',width=30,command=forget)
    btnforget.place(relx=0.25,rely=0.72)
    

    
    
#**********************************OPEN NEW ACCOUNT SCREEN*******
    
    

email_regex=re.compile(r"[^@]+@[^@]+\.[^@]+")

def new_screen():    
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    
    def reset():
        entry_newacn.delete('0',END)
        entry_pass.delete('0',END)
        entry_mob.delete('0',END)
        entry_email.delete('0',END)
        entry_newacn.focus() 
    
    def back():
        frm.destroy()
        login_screen()
        
    def register():
        name=entry_name.get()
        pwd=entry_pass.get()
        mob=entry_mob.get()
        email=entry_email.get()
        if (len(name)==0 or len(pwd)==0 or len(mob)==0 or len(email)==0):
            messagebox.showerror("Failed","Fields Can't be empty")
            return
        elif(len(mob)==11 or len(mob)==12 or len(mob)<=10):
            
            if(len(mob)<10):
                messagebox.showerror("Failed","Mobile Number is not valid")
                return
            
            elif(len(mob)==11 or len(mob)==12):
                pattern=re.compile("(0|91)?[6-9][0-9]{9}")
                
                if not pattern.match(mob):
                    messagebox.showerror("Failed","Mobile Number is not valid")
                    return
                
            elif(len(mob)==10):
                pattern=re.compile("[6-9][0-9]{9}")
                if not pattern.match(mob):
                    messagebox.showerror("Failed","Mobile Number is not valid")
                    return
        
        
            
        
        balance=0.0
        date=time.ctime()
        import sqlite3
        con=sqlite3.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute("insert into account(name,password,mob,email,balance,date) values(?,?,?,?,?,?)",(name,pwd,mob,email,balance,date))
        con.commit()
        con.close()
        
        import sqlite3
        con=sqlite3.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute("select max(acn) from account")
        tup=cur.fetchone()
        con.commit()
        con.close()
        messagebox.showinfo("Success",f"Account OPenet with Acoount Number: {tup[0]}")
        frm.destroy()
        login_screen()
        
        
    lbl_name=Label(frm,text="Name:",font=font,bg=bg)
    lbl_name.place(relx=0.2,rely=0.2)
    
    entry_name=Entry(frm,font=font,bd=3,width=25)
    entry_name.place(relx=0.45,rely=0.2)
    
    lbl_new_pass=Label(frm,text="Password:",font=font,bg=bg)
    lbl_new_pass.place(relx=0.2,rely=0.35)
    
    entry_pass=Entry(frm,font=font,bd=3,width=25,show="*")
    entry_pass.place(relx=0.45,rely=0.35)
    
    lbl_mob=Label(frm,text="Mobile Number:",font=font,bg=bg)
    lbl_mob.place(relx=0.2,rely=0.5)
    
    entry_mob=Entry(frm,font=font,bd=3,width=25)
    entry_mob.place(relx=0.45,rely=0.5)
    
    lbl_email=Label(frm,text="Email ID:",font=font,bg=bg)
    lbl_email.place(relx=0.2,rely=0.65)
    
    entry_email=Entry(frm,font=font,bd=3,width=25)
    entry_email.place(relx=0.45,rely=0.65)
    
    btnlogin=Button(frm,text="Register",font=font,bg='white',width=10,command=register)
    btnlogin.place(relx=0.28,rely=0.78)
    
    btnreset=Button(frm,text="Reset",font=font,bg='white',width=10,command=reset)
    btnreset.place(relx=0.443,rely=0.78)
    
    btnback=Button(frm,text="Back",font=font,bg='white',width=10,command=back)
    btnback.place(relx=0,rely=0.01)
  


#***********************************FORGET PASSWORD SCREEN***********************


    
def forget_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    
    def reset():
        entry_newacn.delete('0',END)
        entry_mob.delete('0',END)
        entry_email.delete('0',END)
        entry_newacn.focus() 
    
    def back():
        frm.destroy()
        login_screen()
        
    def recover_pass():
        mob=entry_mob.get()
        acn=entry_acn.get()
        email=entry_email.get()
        if (len(mob)==0 or len(acn)==0 or len(email)==0):
            messagebox.showerror("Failed","Please Fill all the Deatials")
            return
        else:
            import sqlite3
            con=sqlite3.connect(database='bank.sqlite')
            cur=con.cursor()
            cur.execute("select password from account where acn=? and mob=? and email=?",(acn,mob,email))      
            pwd=cur.fetchone()
            con.commit()
            con.close()
            messagebox.showinfo("Success",f"Your Password is {pwd[0]}")
            frm.destroy()
            login_screen()

        
    
    
    lbl_acn=Label(frm,text="Account Number:",font=font,bg=bg)
    lbl_acn.place(relx=0.2,rely=0.2)
    
    entry_acn=Entry(frm,font=font,bd=3,width=25)
    entry_acn.place(relx=0.45,rely=0.2)
    

    lbl_mob=Label(frm,text="Mobile Number:",font=font,bg=bg)
    lbl_mob.place(relx=0.2,rely=0.35)
    
    entry_mob=Entry(frm,font=font,bd=3,width=25)
    entry_mob.place(relx=0.45,rely=0.35)
    
    lbl_email=Label(frm,text="Email ID:",font=font,bg=bg)
    lbl_email.place(relx=0.2,rely=0.5)
    
    entry_email=Entry(frm,font=font,bd=3,width=25)
    entry_email.place(relx=0.45,rely=0.5)
    
    btnrecover=Button(frm,text="Recover",font=font,bg='white',width=10,command=recover_pass)
    btnrecover.place(relx=0.28,rely=0.7)
    
    btnreset=Button(frm,text="Reset",font=font,bg='white',width=10,command=reset)
    btnreset.place(relx=0.443,rely=0.7)
    
    btnback=Button(frm,text="Back",font=font,bg='white',width=10,command=back)
    btnback.place(relx=0,rely=0.01)
    
    
    
#******************Welcome/Login Screen***********************

def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    lbl=Label(frm,text=f"Welcome, {tup[2]}",font=('',20,'bold','underline'),bg=bg,fg='black')
    lbl.place(relx=.37,rely=.01)
    
    
    
    
    
    def logout():
        frm.destroy()
        login_screen()
    
    
#*****************************Profile Image***********************

    
    if (os.path.exists(f"pics/{tup[0]}.jpg")):
        path=f"pics/{tup[0]}.jpg"
        
    else:
        path=f"pics/default_pic.jpg"
        
    
    img=Image.open(path)
    img=img.resize((170,150))
    imgtk=ImageTk.PhotoImage(img,master=win)
    
    lblpic=Label(frm,image=imgtk)
    lblpic.place(relx=0.02,rely=0.05)
    lblpic.image=imgtk
    
    def setpic():
        imgpath=filedialog.askopenfilename()
        if len(imgpath)==0:
            return
        else:
            newpicname=f'pics/{tup[0]}.jpg'
            if os.path.exists(newpicname):
                os.remove(newpicname)
            shutil.copy(imgpath,newpicname)

            img=Image.open(newpicname)
            img=img.resize((170,150))
            imgtk=ImageTk.PhotoImage(img,master=win)
            lblpic=Label(frm,image=imgtk)
            lblpic.place(relx=0.02,rely=0.05)
            lblpic.image=imgtk
        
    setbtn=Button(frm,text='Set',command=setpic)
    setbtn.place(relx=0.135,rely=0.24)
        
    
#*********************Withdraw Screen************************


    def withdraw_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=0.25,rely=.2,relwidth=.65,relheight=.73)
        bg='white'
        ft=('',20,'bold')
        
        
        def withdraw_amt():
            amt=float(entry_withdraw.get())
            if amt>0:
                import sqlite3
                con=sqlite3.connect(database='bank.sqlite')
                cur=con.cursor()
                cur.execute("select balance from account where acn=?",(tup[0],))
                updatebal=cur.fetchone()[0]
                con.close()
                if (updatebal<amt or amt<=0):
                    messagebox.showerror("Withdrawal Failed",'Amount cannot be more than Balance')
                    return
                    
                new_update_bal=updatebal-amt
                
                
                import sqlite3
                con=sqlite3.connect(database='bank.sqlite')
                cur=con.cursor()
                cur.execute("insert into txn(acn,type,amt,updatedbal,date) values(?,?,?,?,?)",(tup[0],'Dr',amt,new_update_bal,time.ctime()))
                cur.execute("update account set balance=balance-? where acn=?",(amt,tup[0]))                          
                con.commit()
                con.close()
                
                messagebox.showinfo('Success',f'Amount withdrawl Successfully\nRemaining Balance is {new_update_bal}')
                    
                
        
        
        
        lbl=Label(ifrm,text="Withdraw Amount",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.place(relx=.37,rely=.01)
        
        
        lbl_amt=Label(ifrm,text="Enter Amount:",font=ft,bg=bg,fg='red')
        lbl_amt.place(relx=.1,rely=.25)
        
        
        entry_withdraw=Entry(ifrm,font=font,bd=3,width=25)
        entry_withdraw.place(relx=0.45,rely=0.25)
        
        submit_btn=Button(ifrm,text="Submit",font=font,bg='white',width=15,command=withdraw_amt)
        submit_btn.place(relx=0.3,rely=0.48)
        
        
        
#*****************************Deposit Screen***********************
        
        
    def deposit_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=0.25,rely=.2,relwidth=.65,relheight=.73)
        bg='white'
        ft=('',20,'bold')
        
        
        
        def deposit_amt():
            amt=float(entry_withdraw.get())
            if amt>0:
                import sqlite3
                con=sqlite3.connect(database='bank.sqlite')
                cur=con.cursor()
                cur.execute("select balance from account where acn=?",(tup[0],))
                updatebal=cur.fetchone()[0]
                con.close()
                if (amt<=0):
                    messagebox.showerror("Deposit Failed","Deposit Amount can't be o or less than 0")
                    return
                    
                new_update_bal=updatebal+amt
                
                
                import sqlite3
                con=sqlite3.connect(database='bank.sqlite')
                cur=con.cursor()
                cur.execute("insert into txn(acn,type,amt,updatedbal,date) values(?,?,?,?,?)",(tup[0],'Cr',amt,new_update_bal,time.ctime()))
                cur.execute("update account set balance=balance+? where acn=?",(amt,tup[0]))                          
                con.commit()
                con.close()
                
                messagebox.showinfo('Success',f'Amount Deposited Successfully\nRemaining Balance is {new_update_bal}')
                    
        
        lbl=Label(ifrm,text="Deposit Amount",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.place(relx=.37,rely=.01)
        
        
        lbl_amt=Label(ifrm,text="Enter Amount:",font=ft,bg=bg,fg='red')
        lbl_amt.place(relx=.1,rely=.25)
        
        
        entry_withdraw=Entry(ifrm,font=font,bd=3,width=25)
        entry_withdraw.place(relx=0.45,rely=0.25)
        
        submit_btn=Button(ifrm,text="Submit",font=font,bg='white',width=15,command=deposit_amt)
        submit_btn.place(relx=0.3,rely=0.48)    
        
#*********************Balance Screen *************************
   
    
    def balance_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=0.25,rely=.2,relwidth=.65,relheight=.73)
        bg='white'
        ft=('',20,'bold')
        
        import sqlite3
        con=sqlite3.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute("select balance from account where acn=?",(tup[0],))
        bal=cur.fetchone()[0]
        con.commit()
        con.close()
        
        
        lbl=Label(ifrm,text="Account Balance",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.place(relx=.37,rely=.01)
        
        
        lbl_amt=Label(ifrm,text=f"Your Account Balance:\t{bal}",font=('',20,'bold'),bg=bg,fg='black')
        lbl_amt.place(relx=.1,rely=.25)
        
        
        
        
        
#********************************Update Screen**********************

   
    
    
    
    
    def update_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=0.25,rely=.2,relwidth=.65,relheight=.73)
        bg='white'
        ft=('',20,'bold')
        
        lbl=Label(ifrm,text="Update Details",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.place(relx=.37,rely=.01)
        
        import sqlite3
        con=sqlite3.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute('select * from account where acn=?',(tup[0],))
        update_tup=cur.fetchone()
       
        def update():
            name=entry_name.get()
            pwd=entry_pass.get()
            mob=entry_mob.get()
            email=entry_email.get()
            if (len(name)==0 or len(pwd)==0 or len(mob)==0 or len(email)==0):
                messagebox.showerror("Failed","Fields Can't be empty")
                return
            elif(len(mob)==11 or len(mob)==12 or len(mob)<=10):
            
                if(len(mob)<10):
                    messagebox.showerror("Failed","Mobile Number is not valid")
                    return
            
                elif(len(mob)==11 or len(mob)==12):
                    pattern=re.compile("(0|91)?[6-9][0-9]{9}")
                
                    if not pattern.match(mob):
                        messagebox.showerror("Failed","Mobile Number is not valid")
                        return
                
                elif(len(mob)==10):
                    pattern=re.compile("[6-9][0-9]{9}")
                    if not pattern.match(mob):
                        messagebox.showerror("Failed","Mobile Number is not valid")
                        return 
              
            
            import sqlite3
            con=sqlite3.connect(database='bank.sqlite')
            cur=con.cursor()
            cur.execute("update account set name=?,password=?,mob=?,email=? where acn=?",(name,pwd,mob,email,tup[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Success","Account Details Successfully Updated")

        
        lbl_name=Label(ifrm,text="Name:",font=font,bg=bg)
        lbl_name.place(relx=.1,rely=.2)
    
        entry_name=Entry(ifrm,font=font,bd=3,width=25)
        entry_name.place(relx=0.45,rely=0.2)
        entry_name.insert(0,update_tup[2])

        lbl_new_pass=Label(ifrm,text="Password:",font=font,bg=bg)
        lbl_new_pass.place(relx=0.1,rely=0.35)

        entry_pass=Entry(ifrm,font=font,bd=3,width=25,show="*")
        entry_pass.place(relx=0.45,rely=0.35)
        entry_pass.insert(0,update_tup[1])
        
        
        lbl_mob=Label(ifrm,text="Mobile Number:",font=font,bg=bg)
        lbl_mob.place(relx=0.1,rely=0.5)

        entry_mob=Entry(ifrm,font=font,bd=3,width=25)
        entry_mob.place(relx=0.45,rely=0.5)
        entry_mob.insert(0,update_tup[3])

        lbl_email=Label(ifrm,text="Email ID:",font=font,bg=bg)
        lbl_email.place(relx=0.1,rely=0.65)

        entry_email=Entry(ifrm,font=font,bd=3,width=25)
        entry_email.place(relx=0.45,rely=0.65)
        entry_email.insert(0,update_tup[4])
   
        btnupdate=Button(ifrm,text="Update",font=font,bg='white',width=10,command=update)
        btnupdate.place(relx=0.3,rely=0.78)

        
        
        
#****************************************Transaction History*****************************
    
    def transaction_screen():
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=0.25,rely=.2,relwidth=.65,relheight=.73)
        bg='white'
        ft=('',20,'bold')
        
        lbl=Label(ifrm,text="Transaction History",font=('',20,'bold','underline'),bg=bg,fg='red')
        lbl.place(relx=.37,rely=.01)
        
        st=ScrolledText(ifrm,width=85,height=17,font=('arial',15,'bold'))
        st.place(relx=0.01,rely=.12)
        
        msg="  Type\t\tAmount\t\t\tDate\t\t\tUpdated Balance\n\n"
        
        import sqlite3
        con=sqlite3.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute("select type,amt,date,updatedbal from txn where acn=?",(tup[0],))
        tp=reversed(cur.fetchall())
        con.commit()
        con.close()
        
        for tr in tp:
            msg=msg+f"  {tr[0]}\t\t{tr[1]}\t\t{tr[2]}\t\t\t\t     {tr[3]}\n\n"
            
            
        st.insert(END,msg)
            
            
            
            
            
        
        
        
#**************************Welcome Screen ALL Button********************

    withdraw=Button(frm,text="Withdraw",font=font,bg='white',width=15,command=withdraw_screen)
    withdraw.place(relx=0.02,rely=0.28)
    
    deposit=Button(frm,text="Deposit",font=font,bg='white',width=15,command=deposit_screen)
    deposit.place(relx=0.02,rely=0.42)
    
    txn_history=Button(frm,text="txn_history",font=font,bg='white',width=15,command=transaction_screen)
    txn_history.place(relx=0.02,rely=0.56)
    
    balance=Button(frm,text="Balance",font=font,bg='white',width=15,command=balance_screen)
    balance.place(relx=0.02,rely=0.7)
    
    update=Button(frm,text="Update",font=font,bg='white',width=15,command=update_screen)
    update.place(relx=0.02,rely=0.84)

    logout=Button(frm,text="Logout",font=font,bg='white',width=10,command=logout)
    logout.place(relx=0.89,rely=0)


    
login_screen()    
win.mainloop()

