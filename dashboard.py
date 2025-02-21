from tkinter import*
from PIL import Image,ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

class IMS:
    def __init__(self, root, emp_id=None, user_role=None):
        self.root = root
        self.emp_id = emp_id  # Store Employee ID
        self.user_role = user_role  # Store User Role (Admin/Employee)
        self.root.geometry("1350x700+110+80")
        self.root.title(f"Clothing Inventory Management System | {self.user_role}")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # Get Employee Name
        self.emp_name = self.get_employee_name()

        #------------- title --------------
        self.icon_title = PhotoImage(file="images/logo1.png")
        title_text = f"Inventory Management System - {self.emp_name} ({self.user_role})"
        title = Label(self.root, text=title_text, image=self.icon_title, compound=LEFT,
                      font=("times new roman", 30, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        #------------ logout button -----------
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"),
                            bg="yellow", cursor="hand2", command=self.logout)
        btn_logout.place(x=1150, y=10, height=50, width=150)
        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #---------------- left menu ---------------
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        
        if self.user_role == "Admin":
            btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2")
            btn_employee.pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2")
        btn_supplier.pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #----------- content ----------------
        self.lbl_employee=Label(self.root,text="Total Employee\n{ 0 }",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n{ 0 }",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n{ 0 }",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n{ 0 }",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n{ 0 }",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        #------------ footer -----------------
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Group 4S\nFor any Technical Issues Contact: 09617965048",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()
#-------------- functions ----------------
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        if not self.root.winfo_exists():  # Check if window still exists before updating
            return

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {len(product)} ]")

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {len(category)} ]")

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {len(employee)} ]")

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {len(supplier)} ]")

            bill = len(os.listdir("bill"))
            self.lbl_sales.config(text=f"Total Sales\n[ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}")

            # Only call after() if window is still open
            if self.root.winfo_exists():
                self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def get_employee_name(self):
        """ Fetch employee name from database using self.emp_id """
        if not self.emp_id:
            return "Unknown"
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM employee WHERE eid=?", (self.emp_id,))
        emp_name = cur.fetchone()
        con.close()
        return emp_name[0] if emp_name else "Unknown"

    def logout(self):
        """ Logout and return to login screen """
        self.root.destroy()
        import subprocess
        subprocess.run(["python", "login.py"])  # This will run login.py as a separate process

    def check_low_stock(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product WHERE qty::integer <= reorder_level")
            low_stock_items = cur.fetchall()
            if low_stock_items:
                messagebox.showwarning("Low Stock Alert", 
                    f"There are {len(low_stock_items)} items below reorder level!")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def show_sales_analytics(self):
        # Add charts for:
        # - Best selling items
        # - Sales by category
        # - Sales by season
        # - Size distribution
        # - Color popularity
        pass

if __name__ == "__main__":
    root = Tk()
    IMS(root, "E001", "Admin")  # Example test
    root.mainloop()