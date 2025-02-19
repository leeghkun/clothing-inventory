import sqlite3
from tkinter import *
from tkinter import messagebox
import dashboard

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Login")
        self.root.geometry("400x350+500+200")
        self.root.config(bg="white")

        Label(self.root, text="Employee Login", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        Label(self.root, text="Employee ID:", font=("Arial", 12), bg="white").pack()
        self.emp_id_entry = Entry(self.root, font=("Arial", 12), bd=2)
        self.emp_id_entry.pack(pady=5)

        Label(self.root, text="Password:", font=("Arial", 12), bg="white").pack()
        self.password_entry = Entry(self.root, font=("Arial", 12), bd=2, show="*")
        self.password_entry.pack(pady=5)

        Button(self.root, text="Login", command=self.login, font=("Arial", 12, "bold"), bg="green", fg="white").pack(pady=20)

    def login(self):
        emp_id = self.emp_id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not emp_id or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT eid, name, pass, utype FROM employee WHERE eid=?", (emp_id,))
        user = cur.fetchone()
        con.close()

        if user:
            stored_password = user[2]  # Plaintext password from DB
            user_role = user[3]  # Admin or Employee

            if password == stored_password:
                messagebox.showinfo("Success", f"Welcome, {user[1]} ({user_role})")
                self.root.destroy()  # Close login window
                self.open_dashboard(emp_id, user_role)  # Open the dashboard
            else:
                messagebox.showerror("Error", "Invalid Password")
        else:
            messagebox.showerror("Error", "Invalid Employee ID")

    def open_dashboard(self, emp_id, user_role):
        """ Open the Dashboard for All Users """
        root_dashboard = Tk()
        dashboard_app = dashboard.IMS(root_dashboard, emp_id, user_role)  # Pass employee ID & role
        root_dashboard.mainloop()

if __name__ == "__main__":
    root = Tk()
    LoginSystem(root)
    root.mainloop()
