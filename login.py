import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conexion_sqlUsuarios import *
from vendedor import * 
from interfazDBA import*
from gerente import *
path_icono = os.path.join(os.path.dirname(__file__), "coffee-cup.ico")

class Login(Frame):
    
    def __init__(self, master = None):
        super().__init__(master, bg = "#6F4E37", height = 400, width = 840)
        self.master=master
        self.master.resizable(False,False)
        self.master.iconbitmap(path_icono)
        self.pack()
        self.objetos()
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    
    def cerrar_ventana(self):
        cerrar_sesion(self.master,self.con)
        self.master.destroy()

    def elemento_vacio(self,cadena):
        for x in cadena:
            if not x:
                return True
        return False
    def verificar_credenciales(self):
        self.usuario = self.entry_usuario.get()
        self.clave = self.entry_clave.get()

        if self.elemento_vacio([self.usuario, self.clave]):
            messagebox.showerror("Error", "Los campos no pueden estar vacíos")
            return
        
        if self.usuario == "DBA":
                self.master.destroy()
                mainDBA()
                return
        if self.usuario == "Gerente":
                self.master.destroy()
                mainGerente()
                return
        self.con = conectar_db(self.usuario, self.clave)
        if self.con:
            messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
            if self.usuario == "Vendedor":
                self.master.destroy()
                main()
                return
            
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    
    
    def objetos(self):
        self.bloque_principal = Frame(self, bg="#F5EDE1")
        self.bloque_principal.place(x=20, y=20, height=355, width=400)

        Label(self.bloque_principal, text="Usuario:", bg="#F5EDE1").place(x=10, y=50)
        self.entry_usuario = Entry(self.bloque_principal)
        self.entry_usuario.place(x=100, y=50, width=200)

        Label(self.bloque_principal, text="Contraseña:", bg="#F5EDE1").place(x=10, y=100)
        self.entry_clave = Entry(self.bloque_principal, show="*")
        self.entry_clave.place(x=100, y=100, width=200)
        self.ver = Button(self.bloque_principal, text="INICIAR SESION", bg="#C19A6B", command=self.verificar_credenciales)
        self.ver.place(x=135, y=150, height=40, width=135)