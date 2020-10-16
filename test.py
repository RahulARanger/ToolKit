from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
class Counter(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.USERNAME = StringVar()
        self.PASSWORD = StringVar()
        self.PRODUCT_NAME = StringVar()
        self.PRODUCT_PRICE = IntVar()
        self.PRODUCT_QTY = IntVar()
        self.SEARCH = StringVar()
        self.conn = sqlite3.connect("Resources\Database\\admin.db")
        self.cursor = self.conn.cursor()
        self.arrange()
    def arrange(self):
        self.Manage_Frame=Frame(self,bd=4,relief=RIDGE,bg="#660000")
        self.Manage_Frame.place(x=20,y=110,width=450,height=560)
        self.login_btn=Button(self.Manage_Frame,text="Login",font=("times new roman",20,"bold"),pady=20,padx=50,bd=10,relief=GROOVE,command=self.LoginForm)
        self.login_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.Man_Frame=Frame(self,bd=4,relief=RIDGE,bg="#660000")
        self.Man_Frame.place(x=500,y=110,width=840,height=560)
        self.Title = Frame(self, bd=10, relief=GROOVE,bg="#660000",)
        self.Title.pack(side=TOP,fill=X)
        self.lbl_display = Label(self.Title, text="Billing Records", font=('times new roman', 45),bg="#660000",fg="yellow")
        self.lbl_display.pack()    
    
    def LoginForm(self):
        self.Man_Frame=Frame(self,bd=10,relief=RIDGE,bg="#660000")
        self.Man_Frame.pack(expand=True,fill=BOTH)        
        self.lbl_text = Label(self.Man_Frame, text="Administrator Login", font=('times new roman', 18), width=600)
        self.lbl_text.pack(fill=X)
        self.MidLoginForm = Frame(self.Man_Frame,bd=10,relief=GROOVE, width=800,bg="#660000")
        self.MidLoginForm.pack(side=TOP, pady=50)
        self.lbl_username = Label(self.MidLoginForm, text="Username:", font=('times new roman', 25), bd=18,bg="#660000",fg="yellow")
        self.lbl_username.grid(row=0)
        self.lbl_password = Label(self.MidLoginForm, text="Password:", font=('times new roman', 25), bd=18,bg="#660000",fg="yellow")
        self.lbl_password.grid(row=1)
        self.lbl_result = Label(self.MidLoginForm, text="", font=('times new roman', 18),bg="#660000")
        self.lbl_result.grid(row=3, columnspan=2)
        self.username = Entry(self.MidLoginForm, textvariable=self.USERNAME, font=('times new roman', 25), width=15)
        self.username.grid(row=0, column=1)
        self.password = Entry(self.MidLoginForm, textvariable=self.PASSWORD, font=('times new roman', 25), width=15, show="*",)
        self.password.grid(row=1, column=1)
        self.btn_login = Button(self.MidLoginForm, text="Login", font=('times new roman', 18), width=30, command=self.Login)
        self.btn_login.grid(row=2, columnspan=2, pady=20)
        self.btn_login.bind('<Return>', self.Login)
    def Login(self,event=None):
        self.Database()
        if self.USERNAME.get()== "" or self.PASSWORD.get() == "":
            self.lbl_result.config(text="**Please complete the required field!", fg="yellow")
        else:
            self.cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (self.USERNAME.get(), self.PASSWORD.get()))
            if self.cursor.fetchone() is not None:
                self.cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (self.USERNAME.get(), self.PASSWORD.get()))
                data = self.cursor.fetchone()
                self.admin_id = data[0]
                self.USERNAME.set("")
                self.PASSWORD.set("")
                self.lbl_result.config(text="")
                self.ShowHome()
                self.cursor.close()
                self.conn.close() 
            else:
                self.lbl_result.config(text="Invalid username or password", fg="yellow")
                self.USERNAME.set("")
                self.PASSWORD.set("")
    def Database(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_name TEXT, product_qty TEXT, product_price TEXT)")
        self.cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = '12345678'")
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', '12345678')")
            self.conn.commit()
    def ShowHome(self):
        a=Home()        
class Home(Toplevel):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.title("billing records")
        width = 1024
        height = 520
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.resizable(0, 0)
        self.Title = Frame(self, bd=1, relief=SOLID)
        self.Title.pack(pady=10)
        self.lbl_display = Label(self.Title, text="billing records", font=('times new roman', 45))
        self.lbl_display.pack()
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu2 = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Logout", command=self.Logout)
        filemenu.add_command(label="Exit", command=self.Exit2)
        filemenu2.add_command(label="Add new", command=ShowAddNew)
        filemenu2.add_command(label="View", command=ShowView)
        menubar.add_cascade(label="Account", menu=filemenu)
        menubar.add_cascade(label="Inventory", menu=filemenu2)
        self.config(menu=menubar)
        self.config(bg="#6666ff")
    def Exit2(self):
        result = tkMessageBox.askquestion('billing records', 'Are you sure you want to exit?', icon="warning")
        if result == 'yes':
            self.destroy()
            exit()
def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.title("billing record/Add new")
    width = 600
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('times new roman', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=50)
    lbl_productname = Label(MidAddNew, text="Product Name:", font=('times new roman', 25), bd=10)
    lbl_productname.grid(row=0, sticky=W)
    lbl_qty = Label(MidAddNew, text="Product Quantity:", font=('times new roman', 25), bd=10)
    lbl_qty.grid(row=1, sticky=W)
    lbl_price = Label(MidAddNew, text="Product Price:", font=('times new roman', 25), bd=10)
    lbl_price.grid(row=2, sticky=W)
    productname = Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('times new roman', 25), width=15)
    productname.grid(row=0, column=1)
    productqty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('times new roman', 25), width=15)
    productqty.grid(row=1, column=1)
    productprice = Entry(MidAddNew, textvariable=PRODUCT_PRICE, font=('times new roman', 25), width=15)
    productprice.grid(row=2, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('times new roman', 18), width=30, bg="#009ACD", command=AddNew)
    btn_add.grid(row=3, columnspan=2, pady=20)


def AddNew():
    Database()
    self.cursor.execute("INSERT INTO `product` (product_name, product_qty, product_price) VALUES(?, ?, ?)", (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get())))
    conn.commit()
    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_QTY.set("")
    self.cursor.close()
    conn.close()

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="View Products", font=('times new roman', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('times new roman', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('times new roman', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Name", "Product Qty", "Product Price"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('ProductID', text="ProductID",anchor=W)
    tree.heading('Product Name', text="Product Name",anchor=W)
    tree.heading('Product Qty', text="Product Qty",anchor=W)
    tree.heading('Product Price', text="Product Price",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def DisplayData():
    Database()
    self.cursor.execute("SELECT * FROM `product`")
    fetch = self.cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    self.cursor.close()
    conn.close()


def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        self.cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = self.cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        self.cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('billing records', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            self.cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
            conn.commit()
            self.cursor.close()
            conn.close()
    

def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("billing records/View Product")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

def Logout():
    result = tkMessageBox.askquestion('billing records', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()
  



if __name__ == '__main__':
    b=Tk()
    a=Counter(b)
    a.pack(expand=True,fill=BOTH)
    b.mainloop()