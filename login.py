import sqlite3
from tkinter import *
from tkinter import messagebox
import dashboard

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Clothing Inventory Login")
        self.root.geometry("500x600+450+50")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # Title Frame
        title_frame = Frame(self.root, bg="#3C4A54")
        title_frame.place(x=0, y=0, width=500, height=80)
        
        title = Label(title_frame, text="CLOTHING INVENTORY", 
                     font=("Arial", 24, "bold"), 
                     bg="#3C4A54", fg="white")
        title.pack(pady=20)

        # Main Content Frame
        content_frame = Frame(self.root, bg="white")
        content_frame.place(x=50, y=100, width=400, height=400)
        
        # Sign in text
        Label(content_frame, text="Sign in to continue", 
              font=("Arial", 12), 
              bg="white", fg="#666666").pack(pady=(20,40))

        # Employee ID
        Label(content_frame, text="Employee ID", 
              font=("Arial", 11), 
              bg="white", fg="#444444").pack(anchor='w')
        
        self.emp_id_entry = Entry(content_frame, 
                                 font=("Arial", 11),
                                 bg="white",
                                 relief="solid",
                                 bd=1)
        self.emp_id_entry.pack(fill='x', pady=(5,25), ipady=8)  # Added ipady for height

        # Password
        Label(content_frame, text="Password", 
              font=("Arial", 11), 
              bg="white", fg="#444444").pack(anchor='w')
        
        # Password container
        password_container = Frame(content_frame, bg="white", bd=1, relief="solid")
        password_container.pack(fill='x', pady=5)
        
        self.password_entry = Entry(password_container, 
                                  font=("Arial", 11),
                                  bg="white",
                                  bd=0,
                                  show="•")
        self.password_entry.pack(side=LEFT, expand=True, fill='both', ipady=8, padx=2)  # Added ipady for height

        # Eye icon
        self.show_password = False
        self.show_hide_btn = Label(password_container, 
                                 text="👁",
                                 font=("Segoe UI Emoji", 11),
                                 bg="white",
                                 fg="#666666",
                                 cursor="hand2",
                                 padx=8)
        self.show_hide_btn.pack(side=RIGHT, fill='y')
        self.show_hide_btn.bind('<Button-1>', lambda e: self.toggle_password())

        # Login Button
        login_btn = Button(content_frame, 
                          text="LOGIN",
                          command=self.login,
                          font=("Arial", 11),
                          bg="#3C4A54",
                          fg="white",
                          bd=0,
                          cursor="hand2")
        login_btn.pack(fill='x', pady=(40,0), ipady=10)  # Added ipady for height

        # Footer
        footer = Label(self.root, 
                      text="Clothing Inventory Management System | Version 1.0",
                      font=("Arial", 9),
                      bg="white",
                      fg="#666666")
        footer.pack(side=BOTTOM, pady=20)

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.show_hide_btn.config(text="⊘")  # More subtle hide icon
        else:
            self.password_entry.config(show="•")
            self.show_hide_btn.config(text="👁")

    def show_success_message(self, name, role):
        success_window = Toplevel(self.root)
        success_window.title("Success")
        success_window.geometry("300x150+500+200")  # Made smaller
        success_window.config(bg="white")
        success_window.resizable(False, False)
        
        # Title bar
        title_frame = Frame(success_window, bg="#3C4A54", height=40)
        title_frame.pack(fill='x')
        Label(title_frame, text="Success", font=("Arial", 12, "bold"), 
              bg="#3C4A54", fg="white").pack(side=LEFT, padx=15, pady=8)
        
        # Main content
        content_frame = Frame(success_window, bg="white")
        content_frame.pack(fill='both', expand=True)
        
        # Green checkmark
        success_icon = Label(content_frame, text="✓", 
                           font=("Arial", 50),
                           fg="#4CAF50", bg="white")
        success_icon.pack(pady=(15,5))
        
        # Welcome message
        msg = Label(content_frame, 
                   text=f"Welcome, {name}",
                   font=("Arial", 12),
                   bg="white")
        msg.pack()
        
        # Store user info for dashboard
        self.current_user = {"emp_id": self.emp_id_entry.get().strip(),
                           "role": role}

        # Auto proceed to dashboard after 1.5 seconds
        success_window.after(1500, lambda: self.proceed_to_dashboard(success_window))

    def proceed_to_dashboard(self, success_window):
        try:
            success_window.destroy()
            self.root.destroy()
            root_dashboard = Tk()
            dashboard_app = dashboard.IMS(root_dashboard, 
                                        self.current_user["emp_id"], 
                                        self.current_user["role"])
            root_dashboard.mainloop()
        except Exception as e:
            print(f"Dashboard error: {str(e)}")
            messagebox.showerror("Error", "Failed to open dashboard")

    def login(self):
        emp_id = self.emp_id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not emp_id or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            con = sqlite3.connect("ims.db")
            cur = con.cursor()
            
            # Print debug info
            print(f"Attempting login with ID: {emp_id}")
            
            cur.execute("SELECT eid, name, pass, utype FROM employee WHERE eid=?", (emp_id,))
            user = cur.fetchone()
            
            if user:
                print(f"Found user: {user}")
                stored_password = user[2]
                user_role = user[3]

                if password == stored_password:
                    print("Password matched")
                    self.show_success_message(user[1], user_role)
                else:
                    print("Password mismatch")
                    messagebox.showerror("Error", "Invalid Password")
            else:
                print("User not found")
                messagebox.showerror("Error", "Invalid Employee ID")
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    LoginSystem(root)
    root.mainloop()
