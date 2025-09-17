from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter
import pymysql
from time import strftime
from datetime import datetime
from student import student
from face_recognition import Face_Recognition
from attendence import Attendence
from help import Help
import os
import cv2
import numpy as np


def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1400x790+0+0")

        #----variables----------
        self.var_email=StringVar()
        self.var_pass=StringVar()

        img=Image.open(r"college_images\Superior-University.png")
        img=img.resize((500,110))
        self.photoimg=ImageTk.PhotoImage(img)

        self.root.update()                                                                     
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # getting centre of x axis
        x = (window_width - 500) // 2  #centre horizintal

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=x,y=0,width=500,height=130)

        frame=Frame(self.root,bd=2,bg="white")
        frame.place(x=490,y=140,width=340,height=450)

        img1=Image.open(r"college_images\pngtree-avatar-icon-profile-icon-member-login-vector-isolated-png-image_1978396.jpg")
        img1=img1.resize((100,100))
        self.photoimg1=ImageTk.PhotoImage(img1)
        lbl_img1=Label(image=self.photoimg1,borderwidth=0, bg="white")
        lbl_img1.place(x=610,y=145,width=100,height=100)

        get_str=Label(frame,text="Sign in",font=("times new roman",20,"bold"), fg="black",bg="white")
        get_str.place(x=122,y=100)

        #Labels
        #Username

        username=Label(frame,text="Email :",font=("times new roman",12,"bold"),bg="white")
        username.place(x=35,y=155)

        self.txtuser=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",12))
        self.txtuser.place(x=35,y=180,width=270)

         #Password

        password=Label(frame,text="Password :",font=("times new roman",12,"bold"),bg="white")
        password.place(x=35,y=225)

        self.txtpass=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",12),show="*")
        self.txtpass.place(x=35,y=250,width=270)

        #------BUTTONS-------------
        #login
        login_btn=Button(frame,text="Sign in",command=self.login,font=("times new roman",12,"bold"),bg="#000066",fg="white",relief=RIDGE,activebackground="#000066",activeforeground="white")
        login_btn.place(x=110,y=300,width=120,height=35)

        #registerbtn
        registerbtn=Button(frame,text="Sign up",command=self.register_window,font=("times new roman",10,"bold"),fg="#000066",bg="white",borderwidth=0,activebackground="white",activeforeground="#000066")
        registerbtn.place(x=90,y=350,width=160)

        #forgotpassbtn
        passwordbtn=Button(frame,text="Forget password",command=self.forget_password_window,font=("times new roman",10,"bold"),fg="#000066",bg="white",borderwidth=0,activebackground="white",activeforeground="#000066")
        passwordbtn.place(x=90,y=370,width=160)

    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("ERROR","All fields are required")
        elif self.txtuser.get()=="Areeba" and self.txtpass.get()=="irha123":
            messagebox.showinfo("Success","Welcome to Superior Attendence System")
        else:
            conn=pymysql.connect(host="127.0.0.1",user="root",password="Mohibali123@",database="face_recognizer",port=3305)
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                self.var_email.get(),
                self.var_pass.get()
            ))
            row=my_cursor.fetchone()
            if row is None:
                messagebox.showerror("ERROR","Invalid username & password")
            else:
                open_main=1
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=Face_Recognition_System(self.new_window,self)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()

    def forget_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("ERROR","Enter the email address to reset password")
        else:
            conn=pymysql.connect(host="127.0.0.1",user="root",password="Mohibali123@",database="face_recognizer",port=3305)
            my_cursor=conn.cursor() 
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()

            if row==None:
                messagebox.showerror("ERROR","Please eneter the valid username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+470+170")

    def reset_login_fields(self):
        self.var_email.set("")
        self.var_pass.set("")
            
    #-------------reset password function------------
    def reset_pass(self):
        if self.combo_security_Q.get()=="Select":
            messagebox.showerror("ERROR","Select Security Questions",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("ERROR","Enter the answer!",parent=self.root2)
        elif self.txt_new_password.get()=="":
            messagebox.showerror("ERROR","Enter the new password!",parent=self.root2)
        else:
            conn=pymysql.connect(host="127.0.0.1",user="root",password="Mohibali123@",database="face_recognizer",port=3305)
            my_cursor=conn.cursor()
            query=("select * from register where email=%s and securityQ=%s and securityA=%s")
            value=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get())
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("ERROR","Please enter correct answer",parent=self.root2)
            else:
                query=("update register set password=%s where email=%s")
                value=(self.txt_new_password.get(),self.txtuser.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("INFO","Your password has been reset,Login with new password!",parent=self.root2)
                self.root2.destroy()
                self.reset_login_fields()
    #-------------forget password window----------

    def forget_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("ERROR","Enter the email address to reset password")
        else:
            conn=pymysql.connect(host="127.0.0.1",user="root",password="Mohibali123@",database="face_recognizer",port=3305)
            my_cursor=conn.cursor() 
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()

            if row==None:
                messagebox.showerror("ERROR","Please eneter the valid username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+470+170")

                self.root2.configure(bg="white")

                l=Label(self.root2,text="Forget Password",font=("times new roman",18,"bold"), fg="black",bg="white")
                l.place(x=0,y=10,relwidth=1)

                security_Q=Label(self.root2,text="Select Security Questions :",font=("times new roman",11,"bold"),bg="white")
                security_Q.place(x=50,y=80)
                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",11),width=17,state="read only")
                self.combo_security_Q['values']=("Select","Your Birthdate","E","TeacherID") #tuple
                self.combo_security_Q.current(0) #indexing so 0 per select Year  first per hoga
                self.combo_security_Q.place(x=50,y=110,width=270)

                security_A=Label(self.root2,text="Security Answer :",font=("times new roman",11,"bold"),bg="white")
                security_A.place(x=50,y=150)

                self.txt_security=ttk.Entry(self.root2,font=("times new roman",11))
                self.txt_security.place(x=50,y=180,width=270)

                new_password=Label(self.root2,text="New Password :",font=("times new roman",11,"bold"),bg="white")
                new_password.place(x=50,y=220)

                self.txt_new_password=ttk.Entry(self.root2,font=("times new roman",11),show= "*")
                self.txt_new_password.place(x=50,y=250,width=270)

                Reset_btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),width=13,bg="#000066",fg="white")
                Reset_btn.place(x=100,y=320)


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1400x790+0+0")

        #--------variables---------------
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_sequrityQ=StringVar()
        self.var_securityA=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()

        img=Image.open(r"college_images\Superior-University.png")
        img=img.resize((500,110))
        self.photoimg=ImageTk.PhotoImage(img)

        self.root.update()                                                                     
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # getting centre of x axis
        x = (window_width - 500) // 2  #centre horizintal

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=x,y=0,width=500,height=130)

        frame=Frame(self.root,bd=2,bg="white")
        frame.place(x=290,y=120,width=725,height=500)

        get_str=Label(frame,text="Register Here",font=("times new roman",20,"bold"), fg="#000066",bg="white")
        get_str.place(x=290,y=30)

        #-----label and entry fills ----

        fname=Label(frame,text="First Name :",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15))
        fname_entry.place(x=50,y=130,width=270)

        l_name=Label(frame,text="Last Name :",font=("times new roman",15,"bold"),bg="white")
        l_name.place(x=390,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=390,y=130,width=270)

        contact=Label(frame,text="Contact :",font=("times new roman",15,"bold"),bg="white")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=270)

        email=Label(frame,text="Email :",font=("times new roman",15,"bold"),bg="white")
        email.place(x=390,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=390,y=200,width=270)
 
        security_Q=Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white")
        security_Q.place(x=50,y=240)
        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_sequrityQ,font=("times new roman",15),width=17,state="read only")
        self.combo_security_Q['values']=("Select","Your Birthdate","Email","TeacherID") #tuple
        self.combo_security_Q.current(0) #indexing so 0 per select Year  first per hoga
        self.combo_security_Q.place(x=50,y=270,width=270)

        security_A=Label(frame,text="Security Answer :",font=("times new roman",15,"bold"),bg="white")
        security_A.place(x=390,y=240)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15))
        self.txt_email.place(x=390,y=270,width=270)

        pswd=Label(frame,text="Password :",font=("times new roman",15,"bold"),bg="white")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15),show = "*")
        self.txt_pswd.place(x=50,y=340,width=270)

        confirm_pswd=Label(frame,text="Confirm Password: ",font=("times new roman",15,"bold"),bg="white")
        confirm_pswd.place(x=390,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15),show = "*")
        self.txt_confirm_pswd.place(x=390,y=340,width=270)

        #--------check button-------------
        self.var_check=IntVar()
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree the Terms & Conditions",font=("times new roman",12,"bold"),bg="white",onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=380)

        #----buttons--------
        register_btn=Button(frame,text="Register Now",command=self.register_data,font=("times new roman",15,"bold"),bg="#000066",fg="white",relief=RIDGE,activebackground="#000066",activeforeground="white")
        register_btn.place(x=110,y=425,width=150,height=35)

        login_btn=Button(frame,text="Login",font=("times new roman",15,"bold"),bg="#000066",fg="white",relief=RIDGE,activebackground="#000066",activeforeground="white")
        login_btn.place(x=420,y=425,width=150,height=35)

        #----------functions declarations----------
    def register_data(self):
        if self.var_fname.get()=="" or self.var_lname.get()=="" or self.var_sequrityQ.get()=="Select":
            messagebox.showerror("ERROR","All fields are required")
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("ERROR","Password & Confirm password must be same")
        elif self.var_check.get()==0:
            messagebox.showerror("ERROR","Please agree our terms & conditions")
        else:
            conn=pymysql.connect(host="127.0.0.1",user="root",password="Mohibali123@",database="face_recognizer",port=3305)
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=self.var_email.get()
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("ERROR","User already exists try another email")
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                                  self.var_fname.get(),
                                  self.var_lname.get(),
                                  self.var_contact.get(),
                                  self.var_email.get(),
                                  self.var_sequrityQ.get(),
                                  self.var_securityA.get(),
                                  self.var_pass.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Registered Successfully")



class Face_Recognition_System:
    def __init__(self,root,login_window_instance):
        self.root=root
        
        self.root.geometry("1400x790+0+0")
        self.root.title("SUPERIOR ATTENDENCE SYSTEM")
        self.login_window_instance = login_window_instance
        
        img=Image.open(r"college_images\Superior-University.png")
        img=img.resize((500,110))
        self.photoimg=ImageTk.PhotoImage(img)
        
        self.root.update()                                                                     
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # getting centre of x axis
        x = (window_width - 500) // 2  #centre horizintal

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=x,y=0,width=500,height=130)

        title_lbl=Label(self.root,text="SUPERIOR ATTENDENCE SYSTEM",font=("times new roman",25,"bold"), fg="#000066")
        title_lbl.place(x=-100,y=140,width=1530,height=45)

         
       #student dtetails 
       #1

        img2=Image.open(r"college_images\student.png")
        img2=img2.resize((180,180))
        self.photoimg2=ImageTk.PhotoImage(img2)

        b1 = Button(self.root, command=self.student_details, image=self.photoimg2, cursor="hand2")
        b1.place(x=320, y=200, width=180, height=180)

        b1_1 = Button(self.root, command=self.student_details, text="STUDENT DETAILS", cursor="hand2", 
              font=("times new roman", 12, "bold"), bg="#000066", fg="white")
        b1_1.place(x=320, y=355, width=180, height=40)

    

        #face recognition
        #2
        img3=Image.open(r"college_images\facerecognition.webp")
        img3=img3.resize((180,180))
        self.photoimg3=ImageTk.PhotoImage(img3)

        b1=Button(self.root,image=self.photoimg3,command=self.face_data,cursor="hand2")
        b1.place(x=560,y=200,width=180,height=180)
        b1_1 = Button(self.root, text="FACE DETECTOR",command=self.face_data, cursor="hand2", font=("times new roman", 15, "bold"), bg="#000066", fg="white")
        b1_1.place(x=560,y=355,width=180,height=40)

        #ATTENDENCE
        #3
        img4=Image.open(r"college_images\attendence.webp")
        img4=img4.resize((180,180))
        self.photoimg4=ImageTk.PhotoImage(img4)

        b1=Button(self.root,image=self.photoimg4,cursor="hand2",command=self.attendence_data)
        b1.place(x=800,y=200,width=180,height=180)
        b1_1 = Button(self.root, text="ATTENDENCE", cursor="hand2",command=self.attendence_data, font=("times new roman", 15, "bold"), bg="#000066", fg="white")
        b1_1.place(x=800,y=355,width=180,height=40)

        #CONTACT US
        #4
        img5=Image.open(r"college_images\help.webp")
        img5=img5.resize((180,180))
        self.photoimg5=ImageTk.PhotoImage(img5)

        b1=Button(self.root,image=self.photoimg5,cursor="hand2",command=self.help_data)
        b1.place(x=440,y=410,width=180,height=180)
        b1_1 = Button(self.root, text="HELP", cursor="hand2",command=self.help_data, font=("times new roman", 15, "bold"), bg="#000066", fg="white")
        b1_1.place(x=440,y=570,width=180,height=40)

 
       #EXIT
       #8
        img9=Image.open(r"college_images\exit.png")
        img9=img9.resize((180,180))
        self.photoimg9=ImageTk.PhotoImage(img9)

        b1=Button(self.root,image=self.photoimg9,cursor="hand2",command=self.iExit)
        b1.place(x=680,y=410,width=180,height=180)
        b1_1 = Button(self.root, text="EXIT", cursor="hand2",command=self.iExit, font=("times new roman", 12, "bold"), bg="#000066", fg="white")
        b1_1.place(x=680,y=570,width=180,height=40)

    # -------------------FUNTION BUTTONS==================================
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=student(self.new_window)

    
    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)
        #__________OPEPNING IMAGES__________

        #_______EXIT___________
    def iExit(self):
        self.iExit=tkinter.messagebox.askyesno("Face Recognition","Are you sure to exit!",parent=self.root)
        if self.iExit>0:
            self.login_window_instance.reset_login_fields()
            self.root.destroy()
        else:
            return

    def attendence_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendence(self.new_window)

    def help_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Help(self.new_window)

   


if __name__== "__main__":
    main()
