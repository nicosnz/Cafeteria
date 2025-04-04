from tkinter import *
from interfazDBA import *
from login import *


def login():
    raiz = Tk()
    raiz.wm_title("Login")
    app = Login(raiz)
    app.mainloop()
    



if __name__ == "__main__":
    login()
    
   