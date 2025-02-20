from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
from datetime import datetime

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Employee Management")
        self.root.config(bg="#f4f5f7")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("Helvetica",12,"bold"),
                             bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,
                               values=("Select","Email","Name","Contact"),
                               state='readonly',justify=CENTER,font=("Helvetica",12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,
                        font=("Helvetica",12),bg="#f4f5f7")
        txt_search.place(x=200,y=10)
        
        btn_search=Button(SearchFrame,command=self.search,text="Search",
                         font=("Helvetica",12),bg="#4CAF50",fg="white",cursor="hand2")
        btn_search.place(x=410,y=9,width=150,height=30)

        #-------------- title ---------------
        title=Label(self.root,text="Employee Details",font=("Helvetica",15,"bold"),
                   bg="#2196F3",fg="white")
        title.place(x=50,y=100,width=1000)

        #-------------- content ---------------
        #---------- row 1 ----------------
        lbl_empid=Label(self.root,text="Emp ID",font=("Helvetica",12),bg="#f4f5f7")
        lbl_empid.place(x=50,y=150)
        
        txt_empid=Entry(self.root,textvariable=self.var_emp_id,
                       font=("Helvetica",12),bg="white")
        txt_empid.place(x=150,y=150,width=180)

        # DOB with format hint
        lbl_dob=Label(self.root,text="Date of Birth (YYYY-MM-DD)",font=("Helvetica",12),bg="#f4f5f7")
        lbl_dob.place(x=350,y=150)
        
        txt_dob=Entry(self.root,textvariable=self.var_dob,
                     font=("Helvetica",12),bg="white")
        txt_dob.place(x=500,y=150,width=180)

        #---------- row 2 ----------------
        lbl_name=Label(self.root,text="Name",font=("Helvetica",12),bg="#f4f5f7")
        lbl_name.place(x=50,y=190)
        lbl_gender=Label(self.root,text="Gender",font=("Helvetica",12),bg="#f4f5f7")
        lbl_gender.place(x=350,y=190)
        lbl_contact=Label(self.root,text="Contact",font=("Helvetica",12),bg="#f4f5f7")
        lbl_contact.place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,
                      font=("Helvetica",12),bg="white")
        txt_name.place(x=150,y=190,width=180)
        
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,
                               values=("Select","Male","Female","Other"),
                               state='readonly',justify=CENTER,font=("Helvetica",12))
        cmb_gender.place(x=500,y=190,width=180)
        cmb_gender.current(0)
        
        txt_contact=Entry(self.root,textvariable=self.var_contact,
                         font=("Helvetica",12),bg="white")
        txt_contact.place(x=850,y=190,width=180)

        #---------- row 3 ----------------
        lbl_email=Label(self.root,text="Email",font=("Helvetica",12),bg="#f4f5f7")
        lbl_email.place(x=50,y=230)
        lbl_pass=Label(self.root,text="Password",font=("Helvetica",12),bg="#f4f5f7")
        lbl_pass.place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("Helvetica",12),bg="#f4f5f7")
        lbl_utype.place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,
                       font=("Helvetica",12),bg="white")
        txt_email.place(x=150,y=230,width=180)
        
        txt_pass=Entry(self.root,textvariable=self.var_pass,
                      font=("Helvetica",12),bg="white")
        txt_pass.place(x=500,y=230,width=180)
        
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,
                              values=("Admin","Employee"),state='readonly',
                              justify=CENTER,font=("Helvetica",12))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #---------- row 4 ----------------
        lbl_address=Label(self.root,text="Address",font=("Helvetica",12),bg="#f4f5f7")
        lbl_address.place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salary",font=("Helvetica",12),bg="#f4f5f7")
        lbl_salary.place(x=500,y=270)

        self.txt_address=Text(self.root,font=("Helvetica",12),bg="white")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        
        txt_salary=Entry(self.root,textvariable=self.var_salary,
                        font=("Helvetica",12),bg="white")
        txt_salary.place(x=600,y=270,width=180)

        #-------------- buttons -----------------
        btn_add=Button(self.root,text="Save",command=self.add,
                      font=("Helvetica",12,"bold"),bg="#2196F3",fg="white",cursor="hand2")
        btn_add.place(x=500,y=305,width=110,height=28)
        
        btn_update=Button(self.root,text="Update",command=self.update,
                         font=("Helvetica",12,"bold"),bg="#4CAF50",fg="white",cursor="hand2")
        btn_update.place(x=620,y=305,width=110,height=28)
        
        btn_delete=Button(self.root,text="Delete",command=self.delete,
                         font=("Helvetica",12,"bold"),bg="#f44336",fg="white",cursor="hand2")
        btn_delete.place(x=740,y=305,width=110,height=28)
        
        btn_clear=Button(self.root,text="Clear",command=self.clear,
                        font=("Helvetica",12,"bold"),bg="#607d8b",fg="white",cursor="hand2")
        btn_clear.place(x=860,y=305,width=110,height=28)

        #------------ employee details -------------
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        
        self.EmployeeTable=ttk.Treeview(emp_frame,
            columns=("eid","name","email","gender","contact","dob","pass","utype","address","salary"),
            yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        
        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Gender")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="User Type")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("salary",text="Salary")
        
        self.EmployeeTable["show"]="headings"
        
        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=100)
        self.EmployeeTable.column("salary",width=100)
        
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
#-----------------------------------------------------------------------------------------------------
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                # Validate date format
                try:
                    datetime.strptime(self.var_dob.get(), '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Error","Invalid date format. Use YYYY-MM-DD",parent=self.root)
                    return

                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID is already assigned",parent=self.root)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_pass.set(row[6])
        self.var_utype.set(row[7])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[8])
        self.var_salary.set(row[9])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()