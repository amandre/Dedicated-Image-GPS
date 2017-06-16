#!/usr/bin/python
import Tkinter as tk
from PIL import Image, ImageTk
from tkFileDialog import askopenfilename
import urllib2, json, re, pymongo, os, tkMessageBox, numpy

client = pymongo.MongoClient('mongodb://admin:password@ds127802.mlab.com:27802/gps_base')
db = client.gps_base

def about():
    win = tk.Toplevel(app)
    win.geometry('200x70')
    win.resizable(width=False, height=False)
    win.title("About")
    txt = "Version: 1.0"
    L = tk.Label(win, text=txt)
    L.pack(padx=20, pady=20)


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        header = tk.Label(self, text="CD-GPS Scheme based on own image file")
        header.pack(padx=20,pady=20)
        container = tk.Frame(self)
        container.pack()
        self.frames = {}
        for F in (SignInPage, SignUpPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SignUpPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.L1 = tk.Label(self, text="User Name")
        self.L1.pack(anchor=tk.W, padx=(50, 0))
        self.E1 = tk.Entry(self, bd =5)
        self.E1.pack(anchor=tk.E, padx=(0, 50))
        submitBtn = tk.Button(self, text="Sign In", command=self.processLogIn)
        submitBtn.pack(side=tk.BOTTOM, pady=(50, 50))

    def processLogIn(self):
        username= self.E1.get()
        userExists = db.credentials.find_one({"username": username})
        if userExists:
            #usercoords = userExists['coords']
            #if re.match...
            logInSuccessful=1
        if logInSuccessful:
            tkMessageBox.showinfo("USER "+username+" LOGGED IN", "You have been successfully signed in")
        else:
            tkMessageBox.showerror("INCORRECT LOG IN", "Invalid username or password. Please try again.")


class SignUpPage(tk.Frame):
    choice = 0
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.L1 = tk.Label(self, text="User Name")
        self.L1.pack(anchor=tk.W, padx=(50, 0))
        self.E1 = tk.Entry(self, bd =5)
        self.E1.pack(padx=(0, 50))
        self.coords = []
        #TODO 2 - some minor GUI enhancements
        imageBtn = tk.Button(self, text="Choose an image to create your password", command=self.getimage)
        imageBtn.pack(pady=(10,0))
        submitBtn = tk.Button(self, text="Sign Up", command=self.processRegistration)
        submitBtn.pack(side=tk.BOTTOM, pady=(0, 50))

    def toggleonclick(self,event):
        event.widget.focus_set()
        caller = event.widget
        grid_info = caller.grid_info()
        row = grid_info["row"]
        col = grid_info["column"]
        if caller.cget("borderwidth")==2:
            self.coords.remove([row, col])
            caller.config(borderwidth=0)
        else:
            self.coords.append([row, col])
            caller.config(borderwidth=2, relief="solid")
        #print self.coords

    def submitPasswd(self):
        #print self.choice
        #print self.coords
        self.win.destroy()
        username = self.E1.get()
        db.credentials.insert_one({
            "username": username,
            "coords": self.coords
        })
        tkMessageBox.showinfo("USER "+username+" REGISTERED", "You have successfully signed up.\nNow try to log in.")

    def displayimages(self, path):
        self.win = tk.Toplevel()
        self.win.geometry("440x480")
        self.win.resizable(width=False, height=False)
        self.win.title("Coordinates selection")

        #L = tk.Label(self.win, text=txt)
        #L.pack(side=tk.TOP,pady=(20,20))
        tkMessageBox.showinfo("SELECT IMAGES", "Please type your password scheme\nYou need to remember the sequence of selected images\nUnselected images will be excluded from the password sequence")
        imagesList = [f for f in os.listdir(path)]
        N = int(numpy.sqrt(len(imagesList)))
        if N*N==len(imagesList):
            imagesArray= numpy.reshape(imagesList, (N, N))
        #TODO 1 - add ELSE clause for non NxN arrays
        #else:
            # ...
        for row in range(0, len(imagesArray[0])):
            for col in range(0, len(imagesArray[1])):
                rec = imagesArray[row, col]
                img = ImageTk.PhotoImage(Image.open(path+"/"+rec).resize((40, 40)))
                square = tk.Label(self.win, image=img)
                square.image = img
                square.grid(row=row, column=col)
                #TODO 3 - sort elements in the array
                square.bind('<Button-1>', self.toggleonclick)
        fr = tk.Frame(self.win)
        fr.grid(columnspan=N)
        sendCoords = tk.Button(fr, text="CREATE ACCOUNT", command=self.submitPasswd)
        sendCoords.grid()

    def crop(self, path, inputval, N, directory):
        im = Image.open(path+inputval)
        w, h = im.size
        desiredw=w/N
        desiredh=h/N
        k=1
        for i in range(0, h, desiredh):
            for j in range(0, w, desiredw):
                try:
                    os.makedirs(path+directory)
                except WindowsError:
                    pass
                #print str(i)+" "+str(j)
                box = (j, i, j+desiredw, i+desiredh)
                o = im.crop(box)
                o.save(path+directory+"/IMG-"+str(k)+".png", "PNG")
                k += 1
        #TODO 1 contd - or set amount of cells in the image array

    def processRegistration(self):
        try:
            if self.filename and self.E1.get():
                username = self.E1.get()
                #h = 150
                #w = 150
                N = 9
                filestr = re.findall("[\-\_\w\d]*?\.[jpg|png|jpeg|bmp]+", self.filename)
                filestr = ''.join(filestr)
                path = self.filename.replace(filestr, "")
                #self.crop(path, filestr, h, w, username)
                self.crop(path, filestr, N, username)
                self.displayimages(path+username)
        except AttributeError:
            tkMessageBox.showinfo("NO IMAGE PROVIDED", "Please try again, at least 1 image should be chosen")
        else:
            tkMessageBox.showinfo("NO USERNAME OR EMPTY IMAGE", "Please try again.\nPut your desired username and the image to create password")

    def getimage(self):
        self.filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file


if __name__ == "__main__":
    app = MainApp()
    app.title("Own Image GPS Scheme")
    app.tk.call('encoding', 'system', 'utf-8')
    app.geometry('{}x{}'.format(300, 200))
    app.resizable(width=False, height=False)

    menubar = tk.Menu(app)
    filemenu = tk.Menu(menubar, tearoff=0)
    # TODO - fix frames for filemenu
    filemenu.add_command(label="Sign Up", command=lambda: app.controller.show_frame("SignUpPage"))
    filemenu.add_command(label="Sign In", command=lambda: app.controller.show_frame("SignInPage"))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=app.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="About", menu=helpmenu)
    app.config(menu=menubar)

    app.mainloop()