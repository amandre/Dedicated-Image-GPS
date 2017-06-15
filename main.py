#!/usr/bin/python
import Tkinter as tk;
import tkMessageBox

def donothing():
    filewin = tk.Toplevel(root)
    filewin.title('New window')
#   button = Button(filewin, text="Do nothing button")
#   button.pack()

def about():
    win=tk.Toplevel(root)
    win.geometry('{}x{}'.format(200, 70))
    win.resizable(width=False, height=False)
    win.title("About")
    txt="Version: 1.0"
    L=tk.Label(win,text=txt)
    L.pack(padx=20, pady=20)


root = tk.Tk()
root.tk.call('encoding', 'system', 'utf-8')
root.geometry('{}x{}'.format(400, 300))
root.resizable(width=False, height=False)
root.title("CD-GPS Log in Page") #Sign In page is the default page
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Register", command=donothing)
filemenu.add_command(label="Sign In", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="About", menu=helpmenu)
root.config(menu=menubar)

def processLogIn():
    logInSuccessfull=1
    if logInSuccessfull:
        tkMessageBox.showinfo("USER LOGGED IN", "You have been successfully signed in")

header = tk.Label(root, text="Implementation of CD-GPS Scheme")

L1 = tk.Label(root, text="User Name")
L1.pack(side=tk.LEFT, padx=(50, 0))
E1 = tk.Entry(root, bd =5)
E1.pack(side=tk.RIGHT, padx=(0, 50))
#L1.place(relx=0.5)
L2 = tk.Label(root, text="Password")
L2.pack(side=tk.LEFT, padx=(50, 0))
E2 = tk.Entry(root, bd=5)
E2.pack(side=tk.RIGHT, padx=(0, 50))
submitBtn = tk.Button(root, text="Sign In", command=processLogIn)
submitBtn.pack(side=tk.BOTTOM, pady=(0, 50))
#submitBtn.place(rely=0.5)
root.mainloop()