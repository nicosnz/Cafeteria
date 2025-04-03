from tkinter import *
from interfazDBA import *
from login import *
def login():
    raiz = Tk()
    raiz.wm_title("Login")
    app = Login(raiz)
    app.mainloop()
    

def main():
    # Crear la ventana principal
    raiz=Tk()
    raiz.wm_title("Cafetería")

    app=Interfaz(raiz)

    app.mainloop()

if __name__ == "__main__":
    login()
    
   